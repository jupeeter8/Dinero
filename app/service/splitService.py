from fastapi import HTTPException, status
from math import floor

# splitc_category = ["percentage", "ratio", "equally", "unequally"]


# def calculate_split(p: float, o: float, split_type: str, split_value):
#     if split_type not in splitc_category:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid split category"
#         )

#     if split_type == "percentage":
#         percent = float(split_value)
#         check = p * percent
#         check = check / 100
#         if check == o:
#             print("nice")


def verify_split(paid_amount: float, owed_amount: float):
    """
    Due to the nature of currency, it will be easier to store
    vlaues in smallest integer units. For example, it will be
    better to store values in Paise rather than in Rupees
    """
    # Converting the values to Paise
    paid_amount = floor(paid_amount * 100)
    owed_amount = floor(owed_amount * 100)

    # Paid amount must be atleast 1 pasie
    if not paid_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paid Amount can't be less than 1",
        )

    # Owed amount can between inclusive range of [1, paid_amount] in paise
    if not owed_amount > 0 or not owed_amount <= paid_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Owed amount {owed_amount} is not between 1 Paise to {paid_amount} Paise",
        )

    return paid_amount, owed_amount

    # split_type = next(iter(split_method))
    # split_value = split_method[split_type]

    # calculate_split(paid_amount, owed_amount, split_type, split_value)
