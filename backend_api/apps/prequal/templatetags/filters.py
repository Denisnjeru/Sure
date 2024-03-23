from django import template

from apps.prequal.models import FinancialRatio

register = template.Library()


@register.filter(name="total_prequal_score")
def total_prequal_score(supplier, category_id):
    return supplier.total_prequal_score(category_id=category_id)


@register.filter(name="score_rank")
def score_rank(supplier, category_id):
    return supplier.score_rank(category_id=category_id)


@register.filter(name="prequal_section_score")
def prequal_section_score(supplier, section_id):
    return supplier.prequal_section_score(section_id=section_id)


@register.filter(name="prequal_question_response")
def prequal_question_response(supplier, question_id):
    return supplier.prequal_question_response(question_id=question_id)


@register.simple_tag
def financial_ratios(supplier, section, *args, **kwargs):
    equity = kwargs.get("equity", None)
    curr_liabilities = kwargs.get("curr_liabilities", None)
    current_assets = kwargs.get("current_assets", None)
    fixed_assets = kwargs.get("fixed_assets", None)
    debtors = kwargs.get("debtors", None)
    cash = kwargs.get("cash", None)
    turnover = kwargs.get("turnover", None)
    gross_profit = kwargs.get("gross_profit", None)
    net_profit = kwargs.get("net_profit", None)

    ratios = FinancialRatio.objects.filter(section=section, supplier=supplier).first()

    if equity is not None:
        if ratios is not None and ratios.equity is not None:
            equity = round(ratios.equity, 2)
            return f"{equity:,}"
        else:
            return 0

    if curr_liabilities is not None:
        if ratios is not None and ratios.curr_liabilities is not None:
            curr_liabilities = round(ratios.curr_liabilities, 2)
            return f"{curr_liabilities:,}"
        else:
            return 0

    if fixed_assets is not None:
        if ratios is not None and ratios.fixed_assets is not None:
            fixed_assets = round(ratios.fixed_assets, 2)
            return f"{fixed_assets:,}"
        else:
            return 0

    if current_assets is not None:
        if ratios is not None and ratios.current_assets is not None:
            current_assets = round(ratios.current_assets, 2)
            return f"{current_assets:,}"
        else:
            return 0

    if debtors is not None:
        if ratios is not None and ratios.debtors is not None:
            debtors = round(ratios.debtors, 2)
            return f"{debtors:,}"
        else:
            return 0

    if cash is not None:
        if ratios is not None and ratios.cash is not None:
            cash = round(ratios.cash, 2)
            return f"{cash:,}"
        else:
            return 0

    if turnover is not None:
        if ratios is not None and ratios.turnover is not None:
            turnover = round(ratios.turnover, 2)
            return f"{turnover:,}"
        else:
            return 0

    if gross_profit is not None:
        if ratios is not None and ratios.gross_profit is not None:
            gross_profit = round(ratios.gross_profit, 2)
            return f"{gross_profit:,}"
        else:
            return 0

    if net_profit is not None:
        if ratios is not None and ratios.net_profit is not None:
            net_profit = round(ratios.net_profit, 2)
            return f"{net_profit:,}"
        else:
            return 0