from pydantic import BaseModel, Field
from typing import Optional

class InvoiceData(BaseModel):
    """
    Defines the structure of a valid invoice.
    """
    invoice_number: Optional[str] = Field(None, description="Unique Invoice ID")
    invoice_date: Optional[str] = Field(None, description="Date of the invoice")
    total_amount: Optional[float] = Field(None, description="The final amount to pay")
    vendor_name: Optional[str] = Field(None, description="Company issuing the invoice")
    
    @property
    def is_valid(self) -> bool:
        return self.total_amount is not None