import statistics


def update_contractor_stats(session, contractor, Payment):

    all_payments = session.query(Payment).filter_by(contractor_id=contractor.id).all()

    debit_payments = []
    credit_payments = []

    for payment in all_payments:
        if payment.debit:
            debit_payments.append(payment.payment)
        else:
            credit_payments.append(payment.payment)

    if debit_payments:
        contractor.num_debit_payments = len(debit_payments)
        contractor.total_debit_payment = sum(debit_payments)
        contractor.min_debit_payment = min(debit_payments)
        contractor.max_debit_payment = max(debit_payments)
        contractor.median_debit_payment = statistics.median(debit_payments)

    if credit_payments:
        contractor.num_credit_payments = len(credit_payments)
        contractor.total_credit_payment = sum(credit_payments)
        contractor.min_credit_payment = min(credit_payments)
        contractor.max_credit_payment = max(credit_payments)
        contractor.median_credit_payment = statistics.median(credit_payments)

    session.commit()
