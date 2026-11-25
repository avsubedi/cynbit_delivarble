from saas_intelligence import (
    analyze_revio_review,
    score_tenant_payment_risk,
    prioritize_repair_ticket,
    evaluate_code_submission,
)
from agency_and_docs import (
    extract_invoice_to_erp_payload,
    AuditedBusinessAgent,
)
from growth_seo import analyze_search_gaps_and_schema

if __name__ == '__main__':
    # 1. Revio brand & churn intelligence
    print('REVIO:', analyze_revio_review(
        'Oakwood_Apts_04', 2, 'Overcharged on my invoice again and waiting hours for support. Thinking of moving out.'
    ))

    # 2. TenantEase financial & maintenance intelligence
    print('TENANTEASE PAYMENT:', score_tenant_payment_risk(days_late_avg=6.5, missed_payments_12m=2, rent_to_income_ratio=0.45))
    print('TENANTEASE REPAIR:', prioritize_repair_ticket('Water leak under kitchen sink'))

    # 3. Cynbit Studio AST analysis & career matching
    sample_code = 'def process(x):\n    if x > 0:\n        if x < 10:\n            return x\n'
    print('CYNBIT STUDIO:', evaluate_code_submission(sample_code, {'algorithms', 'api_design'}))

    # 4. Document extraction -> ERP payload
    sample_doc = 'Vendor: Apex Cloud Ltd\nInvoice #: INV-2026-884\nTotal Due: $1,450.00'
    print('DOC PIPELINE:', extract_invoice_to_erp_payload(sample_doc))

    # 5. Audited RAG & human-handoff agent
    agent = AuditedBusinessAgent(
        knowledge_base={'appointment': 'Appointments can be booked Mon–Fri 9 AM–5 PM via the client portal.'},
        allowed_tools=['rag_lookup', 'book_appointment'],
    )
    print('AGENT (HIGH CONF):', agent.execute_action('front_desk', 'rag_lookup', 'How do I book an appointment?', 0.92))
    print('AGENT (LOW CONF):', agent.execute_action('front_desk', 'rag_lookup', 'Custom enterprise SLA terms?', 0.51))
    print('AUDIT TRAIL COUNT:', len(agent.audit_log))

    # 6. Search gap & schema intelligence
    print('SEO INTELLIGENCE:', analyze_search_gaps_and_schema(
        target_queries=[
            {'keyword': 'automated invoice processing for SMEs', 'intent': 'transactional'},
            {'keyword': 'what is ai', 'intent': 'informational'},
        ],
        existing_pages=['Full Stack Cloud Engineering', 'Technical SEO Services'],
        service_name='Revio',
        service_url='https://www.cynbit.in/',
    ))