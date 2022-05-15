import os
import yaml
import logging

log = logging.getLogger(__name__)
__properties = {}

PROPERTY_FILE_DEFAULT = 'app_property.yaml'

ENV_VAR_USER_NAME = 'username'
ENV_VAR_PASSWORD = 'password'


def get_user_env():
    return get_property(ENV_VAR_USER_NAME)


def get_pass_env():
    return get_property(ENV_VAR_PASSWORD)


def get_env_var(var_name):
    return os.environ.get(var_name)


def load_properties(property_file_name):
    global __properties

    if not os.path.exists(property_file_name):
        log.info(f"not found property file {property_file_name}")
        return
    log.info(f"found property file {property_file_name}")
    __properties = yaml.load(open(property_file_name), Loader=yaml.FullLoader)


load_properties(PROPERTY_FILE_DEFAULT)


def _get_var_from_property(property_path: list, props: dict):
    prop_value = props.get(property_path[0])
    if isinstance(prop_value, dict):
        return _get_var_from_property(property_path[1:], prop_value)
    else:
        return prop_value


def get_property(property_key: str, default=None):
    local_log = logging.getLogger(__name__ + ".get_property")
    os_var = os.environ.get(property_key.replace(".","_"))
    if os_var:
        local_log.debug(f"found key {property_key} in os variable")
        return os_var
    prop_var = __properties.get(property_key)
    if prop_var:
        local_log.debug(f"found key {property_key} in property file {PROPERTY_FILE_DEFAULT}")
        return prop_var

    prop_key_path = property_key.split(".")
    prop_var = _get_var_from_property(prop_key_path, __properties)

    if prop_var:
        local_log.debug(f"found key {property_key} in property file {PROPERTY_FILE_DEFAULT}")
        return prop_var

    if default is not None:
        local_log.debug(f"for property key {property_key} use default value")
        return default
    error_text = f"not found variable {property_key}, use default value"
    local_log.error(error_text)
    raise Exception(error_text)