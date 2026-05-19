from models.report_model import get_audit_log
from controllers.inventory_controller import (
    controller_get_dashboard_stats, controller_get_category_breakdown
)
from utils.csv_exporter import export_inventory_csv


def controller_get_report():
    """
    Aggregate all data needed for the report page.
    Returns a single dict with stats, breakdown, and audit log.
    """
    return {
        'stats':     controller_get_dashboard_stats(),
        'breakdown': controller_get_category_breakdown(),
        'audit_log': get_audit_log(limit=50),
    }


def controller_export_csv(filepath=None):
    """Export inventory to CSV. Returns filepath or None."""
    return export_inventory_csv(filepath)


def controller_get_audit_log(limit=100):
    return get_audit_log(limit)
