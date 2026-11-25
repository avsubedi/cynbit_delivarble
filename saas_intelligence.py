import ast
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any

# --- 1A. REVIO: Multi-Property Issue Clustering, Churn Signals & Compliance ---
BANNED_CLAIMS = ['guaranteed', '"100% refund"', 'legal liability', 'sue']
ISSUE_TAXONOMY = {
    'waiting_times': ['slow', 'wait', 'delay', 'hours', 'late response'],
    'payment': ['billing', 'overcharged', 'invoice', 'deposit', 'fee'],
    'service': ['rude', 'unhelpful', 'ignored', 'broken', 'dirty'],
}

def analyze_revio_review(property_id: str, rating: int, text: str) -> Dict[str, Any]:
    lower_text = text.lower()
    detected_issues = [
        category for category, keywords in ISSUE_TAXONOMY.items()
        if any(kw in lower_text for kw in keywords)
    ]
    # Early churn/brand-damage risk flag
    churn_risk = 'HIGH' if (rating <= 2 and len(detected_issues) >= 1) or 'cancel' in lower_text or 'moving out' in lower_text else 'LOW'
    
    issue_summary = ', '.join(detected_issues) if detected_issues else 'your recent experience'
    draft_reply = (
        f'Thank you for sharing feedback regarding {property_id}. '
        f'We take concerns around {issue_summary} seriously and have routed this to our property operations lead for review.'
    )
    # Brand & legislative compliance check
    compliant = not any(term in draft_reply.lower() for term in BANNED_CLAIMS)
    
    return {
        'property_id': property_id,
        'detected_issues': detected_issues,
        'churn_risk': churn_risk,
        'draft_reply': draft_reply if compliant else '[BLOCKED: Compliance Review Required]',
        'compliant': compliant,
    }


# --- 1B. TENANTEASE: Non-Payment Risk & Maintenance Prioritization ---
def score_tenant_payment_risk(days_late_avg: float, missed_payments_12m: int, rent_to_income_ratio: float) -> Dict[str, Any]:
    # Lightweight logistic scoring model for bespoke escalation protocols
    z = -2.4 + (0.18 * days_late_avg) + (1.1 * missed_payments_12m) + (3.2 * rent_to_income_ratio)
    prob_non_payment = round(1 / (1 + math.exp(-z)), 3)
    
    if prob_non_payment >= 0.70:
        protocol = 'IMMEDIATE_OUTREACH_AND_PAYMENT_PLAN'
    elif prob_non_payment >= 0.40:
        protocol = 'EARLY_SMS_AND_EMAIL_REMINDER_T_MINUS_5'
    else:
        protocol = 'STANDARD_AUTOMATED_REMINDER'
        
    return {'non_payment_probability': prob_non_payment, 'escalation_protocol': protocol}

def prioritize_repair_ticket(description: str) -> Dict[str, str]:
    desc = description.lower()
    if any(w in desc for w in ['gas leak', 'flood', 'sparks', 'no water', 'fire']):
        return {'priority': 'P1_EMERGENCY', 'sla': '2_HOURS'}
    if any(w in desc for w in ['ac', 'heater', 'fridge', 'lock', 'leak']):
        return {'priority': 'P2_URGENT', 'sla': '24_HOURS'}
    return {'priority': 'P3_ROUTINE', 'sla': '5_DAYS'}


# --- 1C. CYNBIT STUDIO: AST Code Quality Analysis & Role Matching ---
ROLE_PROFILES = {
    'Backend Python Engineer': {'algorithms', 'error_handling', 'clean_code', 'api_design'},
    'AI Automation Engineer': {'error_handling', 'api_design', 'data_pipelines'},
}

def evaluate_code_submission(source_code: str, demonstrated_skills: set) -> Dict[str, Any]:
    tree = ast.parse(source_code)
    branches = sum(isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)) for node in ast.walk(tree))
    has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    missing_docstrings = [fn.name for fn in functions if ast.get_docstring(fn) is None]

    diagnostics = []
    if branches > 5:
        diagnostics.append('Excessive cyclomatic complexity; refactor nested conditions.')
    if not has_try_except:
        diagnostics.append('Lack of provision for exceptional circumstances (no try/except blocks).')
    if missing_docstrings:
        diagnostics.append(f'Poor ease of maintenance: missing docstrings in {missing_docstrings}.')

    # Career matching
    role_matches = {}
    for role, reqs in ROLE_PROFILES.items():
        pass
    