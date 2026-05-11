# Config Overrides

Use `--config` with YAML to provide user-known business context.

## CLI usage

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --output-dir outputs/crm_contacts_with_config
```

## YAML structure

```yaml
dataset:
  name: crm_contacts
  display_name: CRM Contacts
  description: Synthetic CRM contact export used for documentation testing.
  owner: Example Data Team
  domain: CRM
  source_system: Salesforce

columns:
  contact_id:
    display_name: Contact ID
    description: Unique identifier for a CRM contact record.
    semantic_role: identifier

  email:
    display_name: Email Address
    description: Contact email used for communications.
    semantic_role: possible_sensitive
    sensitivity_hint: possible_personal_data
    review_required: true
    review_notes:
      - Confirm handling rules before sharing.
```

## Dataset-level fields

- `name`
- `display_name`
- `description`
- `owner`
- `domain`
- `source_system`

## Allowed column-level fields

- `display_name`
- `description`
- `semantic_role`
- `semantic_role_confidence`
- `sensitivity_hint`
- `review_required`
- `review_notes`
- `caveats`
- `allowed_values`
- `business_rules`
- `owner`
- `domain`
- `source_system`

## What config can override

Config can override business-context metadata in dictionary outputs (display name, description, semantic metadata, review annotations, and business rules).

## What config cannot override

Config does **not** overwrite observed profiling evidence, including:
- `row_count`
- `null_count`
- `distinct_count`
- `sample_values`
- observed physical profiling facts (types and distribution-derived metrics)

## Provenance fields

`data_dictionary.json` includes explicit provenance:
- `description_source` (`deterministic_template`, `blank_review_required`, `config_override`)
- `display_name_source` (`generated`, `config_override`)
- `semantic_role_source` (`deterministic_inference`, `config_override`)
