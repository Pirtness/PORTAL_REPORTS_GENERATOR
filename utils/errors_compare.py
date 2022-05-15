from utils.fingerprint_algorithm import hashed_texts_are_similar, get_hash_set_from_string


def generate_data_for_tables_with_errors_templates(test_to_errors, templates={}, min_similarity_percentage=70, shingle_length=5):
    test_to_templates = {}
    test_to_templates_rows = []
    new_templates_rows = []

    last_template_id = 1 if len(templates) == 0 else max(templates.keys())
    for test in test_to_errors:
        test_to_templates[test] = set()
        if len(test_to_errors[test]) == 0:
            if 1 not in test_to_templates[test]:
                test_to_templates_rows.append({'id_test': test, 'error_text': '', 'id_template': 1})
                test_to_templates[test].add(1)
                if 1 not in templates:
                    templates[1] = ''
                    new_templates_rows.append({'id': 1, 'error_template': '',
                                               'hashed_error_template': '', 'description': None})
            continue
        for error in test_to_errors[test]:
            hashed_error = get_hash_set_from_string(error[0:700], shingle_length)
            template_found = False
            for template_id in templates:
                if template_id == 1:
                    continue
                if hashed_texts_are_similar(hashed_error, templates[template_id], min_similarity_percentage):
                    if (template_id not in test_to_templates[test]):
                        test_to_templates_rows.append({'id_test': test, 'error_text': error, 'id_template': template_id})
                        test_to_templates[test].add(template_id)
                    template_found = True
            if not template_found:
                last_template_id += 1
                templates[last_template_id] = hashed_error
                new_templates_rows.append({'id': last_template_id, 'error_template': error, 'hashed_error_template': ', '.join(hashed_error), 'description': None})
                test_to_templates[test].add(last_template_id)
                test_to_templates_rows.append({'id_test': test, 'error_text': error, 'id_template': last_template_id})
    return test_to_templates_rows, new_templates_rows