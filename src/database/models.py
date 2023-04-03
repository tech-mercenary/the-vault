from sqlalchemy import DateTime, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing_extensions import Annotated
from decimal import Decimal
from config import Side, AccountType

type_pk = Annotated[int, mapped_column(primary_key=True)]
type_name = Annotated[str, mapped_column(nullable=False, unique=True)] 
type_desc = Annotated[str|None, mapped_column(nullable=False, default="")]
type_timestamp = Annotated[datetime, mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),]
str_30 = Annotated[str, 30]
num_6_2 = Annotated[Decimal, 6]


class Base(DeclarativeBase):
    pass


class Currency(Base):
    __tablename__ = "currency"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    description: Mapped[type_desc]

from sqlalchemy.orm import foreign, remote


class AccountGroup(Base):
    __tablename__ = "account_group"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[type_name]
    description: Mapped[type_desc]
    parent_id : Mapped[int|None] = mapped_column(ForeignKey("account_group.id"))

    # TODO: Check if omitting the "AccountGroup" in `relationship` is a problem
    parent: Mapped["AccountGroup"] = relationship("AccountGroup", remote_side="AccountGroup.id", back_populates="children")
    children: Mapped[list["AccountGroup"]] = relationship("AccountGroup", back_populates="parent")
    accounts: Mapped[list["Account"]] = relationship(back_populates="account_group")

    @property
    def alias(self):
        if self.parent_id is not None:
            return f"{self.parent.alias}>{self.name}"
        return self.name


class Account(Base):
    """
    Account model
        opened_at: The date the account was opened in UTC
        closed_at: The date the account was closed in UTC
        account_type: The formal accounting type of the account
    """
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str|None] = mapped_column(nullable=False, default="")
    account_number: Mapped[str|None] = mapped_column(nullable=False, default="")
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    opened_at: Mapped[str]
    closed_at: Mapped[str|None]
    account_group_id: Mapped[int] = mapped_column(ForeignKey("account_group.id"))
    account_type: Mapped[AccountType]
    
    currency: Mapped["Currency"] = relationship("Currency")
    account_group: Mapped["AccountGroup"] = relationship(back_populates="accounts")
    
    @property
    def alias(self):
        return f"{self.account_group.alias}>{self.name}"

# TODO: Implement model AccountOverdraft -- Replace AccountOverdraft with AccountLimitHistory  
# TODO: Implement model TransactionGroup
# TODO: Implement model Transaction
# TODO: Implement model Employer
# TODO: Implement model Salary
# TODO: Implement model CreditCard
# TODO: Implement model CreditCardSummary
# TODO: Implement model CreditCardSummaryBalance
# TODO: Implement model CreditCardSummaryTransaction
# TODO: Implement model FixedTerm (TBD)
# TODO: Implement model SupplyPurchase (TBD)
# TODO: Implement model SupplyConsumption (TBD)
# TODO: Implement model PhysicalAsset (TBD)
# TODO: Implement model Monotax (TBD)
# TODO: Implement model AFIPInvoice (TBD)
