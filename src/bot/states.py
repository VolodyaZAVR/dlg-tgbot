from aiogram.fsm.state import StatesGroup, State


class SetLang(StatesGroup):
    lang = State()


class QRcode(StatesGroup):
    scan = State()


class Authorization(StatesGroup):
    licence_input = State()
    confirm = State()


class RegistrationForm(StatesGroup):
    user_agree = State()
    name = State()
    surname = State()
    middle_name = State()
    number = State()
    confirm = State()
    edit_name = State()
    edit_surname = State()
    edit_middle_name = State()
    edit_number = State()
    select_format = State()
    licence_input = State()


class Orders(StatesGroup):
    contact_point = State()
    job_type = State()
    order = State()
    confirm = State()
    edit_contact_point = State()
    edit_job_type = State()
    edit_order = State()
    add_order = State()
    order_to_edit = State()
    order_to_delete = State()
    licence_series = State()
    licence_number = State()
    partners = State()


class VehicleInfo(StatesGroup):
    select_format_vehicle = State()
    vehicle_number = State()
    trailer = State()
    select_format_trailer = State()
    trailer_number = State()
    vehicle_weight = State()
    edit_name = State()
    edit_surname = State()
    edit_middle_name = State()
    edit_number = State()
    edit_format_vehicle = State()
    edit_vehicle_number = State()
    edit_trailer = State()
    edit_format_trailer = State()
    edit_trailer_number = State()
    edit_vehicle_weight = State()
    contact_point = State()
    job_type = State()
    licence_series = State()
    licence_number = State()


class Admin(StatesGroup):
    fast_activation = State()
    fast_registration = State()
    fast_orders = State()
    fast_vehicle = State()
    id_searching = State()
    surname_searching = State()
    licence_searching = State()
    add_user = State()
    edit_user = State()
    edit_user_name = State()
    edit_user_surname = State()
    edit_user_middle_name = State()
    edit_user_number = State()
    edit_user_licence_series = State()
    edit_user_licence_number = State()
    delete_user = State()
    block_user = State()
    order_by_key = State()
    order_by_number = State()
    order_by_driver = State()
    edit_order = State()
    delete_order = State()
    purge_key = State()
    add_stand = State()
    remove_stand = State()
    add_admin = State()
    remove_admin = State()
    add_manager = State()
    remove_manager = State()


class Manager(StatesGroup):
    fast_activation = State()
    fast_registration = State()
    fast_orders = State()
    fast_vehicle = State()
    id_searching = State()
    surname_searching = State()
    licence_searching = State()
    add_user = State()
    edit_user = State()
    edit_user_name = State()
    edit_user_surname = State()
    edit_user_middle_name = State()
    edit_user_number = State()
    edit_user_licence_series = State()
    edit_user_licence_number = State()
    delete_user = State()
    order_by_key = State()
    order_by_number = State()
    order_by_driver = State()
    edit_order = State()
    delete_order = State()
    purge_key = State()
