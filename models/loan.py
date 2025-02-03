from dataclasses import dataclass
from datetime import datetime

@dataclass
class Loan:
    id: int = None
    name: str = ""
    phone: str = ""
    total_amount: float = 0.0
    installments: int = 0
    created_at: datetime = None

    @property
    def installment_value(self):
        return self.total_amount / self.installments if self.installments else 0