import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

# --- 2A. STANDARDIZED DOCUMENT -> ERP/CRM MODULE ---
def extract_invoice_to_erp_payload(raw_document_text: str) -> Dict[str, Any]:
    invoice_id = re.search(r'Invoice\s*#:\s*([A-Z0-9-]+)', raw_document_text)
    vendor = re.search(r'Vendor:\s*(.+)', raw_document_text)
    total = re.search(r'Total\s*Due:\s*\$?([\d,]+\.\d{2})', raw_document_text)

    extracted = {
        'erp_invoice_id': invoice_id.group(1) if invoice_id else None,
        'crm_vendor_name': vendor.group(1).strip() if vendor else None,
        'amount_usd': float(total.group(1).replace(',', '')) if total else None,
    }
    # Validation gate before ERP sync
    is_valid = all(v is not None for v in extracted.values())
    return {
        'status': 'READY_FOR_ERP_SYNC' if is_valid else 'NEEDS_HUMAN_VERIFICATION',
        'payload': extracted,
    }


# --- 2B. PERMISSIONED & AUDIT-LOGGED AGENCY AI (RAG + VOICE/CHAT HANDOFF) ---
class AuditedBusinessAgent:
    def __init__(self, knowledge_base: Dict[str, str], allowed_tools: List[str]):
        self.knowledge_base = knowledge_base
        self.allowed_tools = set(allowed_tools)
        self.audit_log: List[Dict[str, Any]] = []

    def _log_event(self, actor: str, action: str, status: str, metadata: Dict[str, Any]):
        self.audit_log.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'actor': actor,
            'action': action,
            'status': status,
            'metadata': metadata,
        })

    def execute_action(self, user_role: str, tool_name: str, query: str, confidence: float) -> Dict[str, Any]:
        # 1. Permission Check
        if tool_name not in self.allowed_tools or (tool_name == 'issue_refund' and user_role != 'manager'):
            self._log_event(user_role, tool_name, 'DENIED_PERMISSION', {'query': query})
            return {'status': 'BLOCKED', 'reason': 'Insufficient permissions for requested tool.'}

        # 2. Confidence Threshold -> Human Intervention Handoff
        if confidence < 0.75:
            self._log_event(user_role, tool_name, 'ESCALATED_TO_HUMAN', {'confidence': confidence, 'query': query})
            return {
                'status': 'HUMAN_HANDOFF',
                'message': 'Routing conversation to a live specialist with full context.',
            }

        # 3. Grounded Internal RAG Lookup (Hallucination Reduction)
        matched_context = next(
            (ans for key, ans in self.knowledge_base.items() if key in query.lower()),
            None,
        )
        if not matched_context:
            self._log_event(user_role, tool_name, 'ESCALATED_NO_GROUNDING', {'query': query})
            return {'status': 'HUMAN_HANDOFF', 'message': 'No verified policy found; escalating to human agent.'}

        self._log_event(user_role, tool_name, 'EXECUTED', {'confidence': confidence})
        return {'status': 'SUCCESS', 'response': matched_context}