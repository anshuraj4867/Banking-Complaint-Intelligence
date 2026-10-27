
REGULATORY_REFERENCES = {
    "Trouble during payment process": {
        "topic": "Payment processing and error resolution",
        "jurisdiction": "United States",
        "reference": "Electronic Fund Transfer Act / Regulation E, where applicable",
        "explanation": (
            "Potentially relevant when a complaint concerns an electronic "
            "fund transfer, unauthorized transfer, or an applicable error "
            "resolution process. Coverage depends on the facts and transaction."
        ),
        "url": "https://www.consumerfinance.gov/rules-policy/regulations/1005/"
    },
    "Managing an account": {
        "topic": "Account terms and deposit account practices",
        "jurisdiction": "United States",
        "reference": "Consumer Financial Protection Bureau resources",
        "explanation": (
            "Review the applicable account agreement and consumer protection "
            "requirements based on the type of account and complaint."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/"
    },
    "Written notification about debt": {
        "topic": "Debt collection notices",
        "jurisdiction": "United States",
        "reference": "Fair Debt Collection Practices Act resources",
        "explanation": (
            "Potentially relevant to covered debt collectors and required "
            "debt-related notices. Applicability depends on the collector, "
            "debt, and circumstances."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/debt-collection/"
    },
    "Attempts to collect debt not owed": {
        "topic": "Debt collection disputes",
        "jurisdiction": "United States",
        "reference": "Fair Debt Collection Practices Act resources",
        "explanation": (
            "May be relevant when a consumer disputes a debt or alleges "
            "collection of an amount not owed. The applicable rules depend "
            "on the facts and the parties involved."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/debt-collection/"
    },
    "Communication tactics": {
        "topic": "Debt collection communications",
        "jurisdiction": "United States",
        "reference": "Fair Debt Collection Practices Act resources",
        "explanation": (
            "Potentially relevant to allegations about collection calls, "
            "communications, or conduct by a covered debt collector."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/debt-collection/"
    },
    "Incorrect information on credit report": {
        "topic": "Credit reporting accuracy",
        "jurisdiction": "United States",
        "reference": "Fair Credit Reporting Act resources",
        "explanation": (
            "Potentially relevant to inaccurate information in a consumer "
            "report and the applicable dispute and investigation process."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/"
    },
    "Incorrect information on your report": {
        "topic": "Consumer report accuracy",
        "jurisdiction": "United States",
        "reference": "Fair Credit Reporting Act resources",
        "explanation": (
            "Review the alleged reporting error and the applicable "
            "consumer reporting dispute process."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/"
    },
    "Improper use of your report": {
        "topic": "Permissible use of consumer reports",
        "jurisdiction": "United States",
        "reference": "Fair Credit Reporting Act resources",
        "explanation": (
            "Potentially relevant when a complaint alleges that a consumer "
            "report was accessed or used improperly."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/"
    },
    "Problem with a purchase shown on your statement": {
        "topic": "Billing disputes and electronic transfers",
        "jurisdiction": "United States",
        "reference": "Consumer Financial Protection Bureau resources",
        "explanation": (
            "The applicable requirements depend on whether the issue "
            "involves a card billing dispute, an electronic transfer, "
            "or another type of transaction."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/"
    },
    "Problem with a credit reporting company's investigation into an existing problem": {
        "topic": "Credit reporting dispute investigations",
        "jurisdiction": "United States",
        "reference": "Fair Credit Reporting Act resources",
        "explanation": (
            "Potentially relevant to complaints about the investigation "
            "of disputed information in a consumer report."
        ),
        "url": "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/"
    }
}


def get_regulatory_reference(category):
    return REGULATORY_REFERENCES.get(category)
