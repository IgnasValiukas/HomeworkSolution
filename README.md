A Python program that processes shipment records and applies discounts based on size, provider, and monthly limits.

---

## Task Requirements

1. **S-size shipments** must always be priced at the lowest S-size price among all providers.
2. **Every 3rd L-size shipment via LP** in a calendar month is **free**.
3. **Total monthly discounts** are capped at **10 €**.
   - If there's not enough discount budget, a **partial discount** is applied.

---

## Design Decisions & Assumptions

- **Date parsing**: Uses the `'YYYY-MM'` format from each shipment line.
- **Valid providers**: Only `"LP"` and `"MR"` are accepted.
- **Discount tracking** is managed per month.
- **No external libraries** are used (except `unittest` for testing).
- Code is structured to make adding new rules or providers simple.

---

## Code Language & Version
- Language - Python
- Version - Python 3.13.3
  

---

## Commands  

- To run: python main.py
- To test: python -m unittest test_main.py

---

##  Contact

Created by Ignas V   
Email: ignas.valiukas@gmail.com  

---


## File Structure

```bash
.
├── input.txt          # Shipment data input file
├── main.py            # Main logic to read input and apply discounts
├── unit_test.py       # Unit tests for discount functionality
├── README.md          # This file

