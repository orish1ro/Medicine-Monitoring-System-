import json
from models.medicine_model import (
    add_medicine, get_all_medicines, get_medicine_by_id,
    update_medicine, delete_medicine, search_medicines
)
from models.report_model import log_audit
from utils.validators import validate_medicine
from controllers.auth_controller import require_login


def controller_add_medicine(data):
    """
    Validate and add a new medicine.
    Returns (True, medicine_id) or (False, error_message).
    """
    user = require_login()

    valid, error = validate_medicine(data)
    if not valid:
        return False, error

    med_id = add_medicine(
        name=data['name'].strip(),
        category_id=int(data['category_id']),
        manufacturer_id=int(data['manufacturer_id']),
        unit_id=int(data['unit_id']),
        quantity=int(data.get('quantity', 0)),
        expiry_date=data['expiry_date'],
        price=float(data.get('price', 0)),
        batch_number=data['batch_number'].strip(),
        low_stock_threshold=int(data.get('low_stock_threshold', 10))
    )

    if not med_id:
        return False, "Failed to save medicine to database."

    log_audit(user['id'], 'INSERT', med_id, json.dumps({'name': data['name']}))
    return True, med_id


def controller_update_medicine(medicine_id, data):
    """
    Validate and update an existing medicine.
    Returns (True, None) or (False, error_message).
    """
    user = require_login()

    valid, error = validate_medicine(data)
    if not valid:
        return False, error

    old = get_medicine_by_id(medicine_id)
    if not old:
        return False, "Medicine not found."

    success = update_medicine(
        medicine_id=medicine_id,
        name=data['name'].strip(),
        category_id=int(data['category_id']),
        manufacturer_id=int(data['manufacturer_id']),
        unit_id=int(data['unit_id']),
        quantity=int(data.get('quantity', 0)),
        expiry_date=data['expiry_date'],
        price=float(data.get('price', 0)),
        batch_number=data['batch_number'].strip(),
        low_stock_threshold=int(data.get('low_stock_threshold', 10))
    )

    if not success:
        return False, "Failed to update medicine."

    changes = json.dumps({'before': old['name'], 'after': data['name']})
    log_audit(user['id'], 'UPDATE', medicine_id, changes)
    return True, None


def controller_delete_medicine(medicine_id):
    """
    Delete a medicine by ID.
    Returns (True, None) or (False, error_message).
    """
    user = require_login()

    med = get_medicine_by_id(medicine_id)
    if not med:
        return False, "Medicine not found."

    success = delete_medicine(medicine_id)
    if not success:
        return False, "Failed to delete medicine."

    log_audit(user['id'], 'DELETE', None, json.dumps({'deleted': med['name']}))
    return True, None


def controller_get_all_medicines():
    return get_all_medicines()


def controller_get_medicine(medicine_id):
    return get_medicine_by_id(medicine_id)


def controller_search_medicines(query="", category_id=None):
    return search_medicines(query, category_id)
