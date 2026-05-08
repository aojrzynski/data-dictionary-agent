# Example Commands

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/crm_contacts_profile
```

```bash
data-dictionary-agent --input sample_data/ecommerce_orders/orders.csv --output-dir outputs/orders_profile
```

Expected output files in each output directory:
- `profiling_trace.json`
- `data_dictionary.md`
- `data_dictionary.csv`
- `data_dictionary.json`
