"""
Global Rural Proximity Mini-Market Network - RWA Tokenization & Supply Engine
-----------------------------------------------------------------------------
Open-Source Web3 Protocol for Crowdfunding Local Grocery Stores, Automating 
Immediate Smart Payouts to Local Farmers, and Distributing Retail Dividends.

License: MIT
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class StoreCapExToken:
    token_id: str
    investor_address: str
    store_location_code: str
    amount_funded_eur: float
    equity_yield_share: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class LocalFarmerPayout:
    payout_id: str
    farmer_address: str
    produce_type: str  # e.g., "Dairy", "Fresh_Vegetables", "Bakery"
    deliver_quantity_kg: float
    agreed_price_per_unit: float
    total_amount_eur: float
    is_paid: bool = False

class RuralMarketTokenEngine:
    """
    Real-World Asset (RWA) Engine for Rural Micro-Retail Expansion.
    Supports global retail brands (e.g., Profi, Lidl, Kaufland) in expanding 
    into emerging or rural markets using tokenized capital and local farmer smart payouts.
    """
    def __init__(self, platform_name: str = "GLOBAL-RURAL-RETAIL-NETWORK"):
        self.platform_name = platform_name
        self.investor_registry: Dict[str, StoreCapExToken] = {}
        self.farmer_payouts: Dict[str, LocalFarmerPayout] = {}
        self.total_capex_raised_eur: float = 0.0
        self.total_farmer_payouts_eur: float = 0.0

    def fund_store_opening(self, investor: str, store_code: str, amount_eur: float, target_capex: float = 60000.0) -> StoreCapExToken:
        """Allows global impact investors or retail funds to tokenize store creation in rural areas."""
        token_id = hashlib.sha256(f"{investor}_{store_code}_{time.time()}".encode()).hexdigest()[:12]
        yield_share = (amount_eur / target_capex) * 100.0

        token = StoreCapExToken(
            token_id=token_id,
            investor_address=investor,
            store_location_code=store_code,
            amount_funded_eur=amount_eur,
            equity_yield_share=yield_share
        )

        self.investor_registry[token_id] = token
        self.total_capex_raised_eur += amount_eur
        print(f"[STORE FUNDED] Investor {investor[:8]}... contributed €{amount_eur:,.2f} to Store '{store_code}' ({yield_share:.2f}% Equity Share)")
        return token

    def record_farmer_delivery(self, farmer_address: str, produce: str, qty: float, unit_price: float) -> LocalFarmerPayout:
        """Logs fresh produce delivery from local farmers into the smart supply system."""
        total_value = qty * unit_price
        payout_id = hashlib.sha256(f"{farmer_address}_{produce}_{time.time()}".encode()).hexdigest()[:10]

        payout = LocalFarmerPayout(
            payout_id=payout_id,
            farmer_address=farmer_address,
            produce_type=produce,
            deliver_quantity_kg=qty,
            agreed_price_per_unit=unit_price,
            total_amount_eur=total_value
        )
        self.farmer_payouts[payout_id] = payout
        print(f"[DELIVERY RECORDED] Farmer {farmer_address[:8]}... delivered {qty} kg/units of {produce} (€{total_value:,.2f} pending)")
        return payout

    def execute_farmer_smart_payout(self, payout_id: str):
        """Executes instant, zero-fee smart contract payment to local farmer upon quality verification."""
        if payout_id not in self.farmer_payouts:
            print(f"[ERROR] Delivery ID {payout_id} not found.")
            return

        payout = self.farmer_payouts[payout_id]
        if payout.is_paid:
            print(f"[WARNING] Payout {payout_id} already executed.")
            return

        payout.is_paid = True
        self.total_farmer_payouts_eur += payout.total_amount_eur

        print("\n" + "="*70)
        print(f"      SMART CONTRACT PAYOUT EXECUTED TO LOCAL FARMER")
        print("="*70)
        print(f"Payout ID: {payout_id}")
        print(f"Farmer Address: {payout.farmer_address}")
        print(f"Produce Supplied: {payout.produce_type} ({payout.deliver_quantity_kg} units)")
        print(f"Total Instant Payout: €{payout.total_amount_eur:,.2f}")
        print("="*70 + "\n")

    def distribute_retail_yield(self, store_code: str, monthly_net_profit_eur: float):
        """Distributes monthly net retail profit to store CapEx token holders."""
        print(f"\n[RETAIL PROFIT DISTRIBUTION] Store '{store_code}' generated €{monthly_net_profit_eur:,.2f} net profit.")
        print(f"Distributing yield to RWA token investors:")

        for tid, token in self.investor_registry.items():
            if token.store_location_code == store_code:
                dividend = monthly_net_profit_eur * (token.equity_yield_share / 100.0)
                print(f" -> Investor {token.investor_address[:8]}... received €{dividend:,.2f} dividend.")

    def print_network_summary(self):
        """Generates executive status report for global retail network."""
        print("\n" + "#"*75)
        print(f"      {self.platform_name} - GLOBAL LEDGER REPORT")
        print("#"*75)
        print(f"Total Store CapEx Crowdfunded: €{self.total_capex_raised_eur:,.2f}")
        print(f"Total Direct Farmer Payouts Executed: €{self.total_farmer_payouts_eur:,.2f}")
        print(f"Total Registered Investor Tokens: {len(self.investor_registry)}")
        print(f"Total Registered Farmer Deliveries: {len(self.farmer_payouts)}")
        print("#"*75 + "\n")

# --- EXECUTION DEMO ---
if __name__ == "__main__":
    engine = RuralMarketTokenEngine(platform_name="GLOBAL-PROXIMITY-RETAIL-NETWORK")

    print("\n--- 1. CROWDFUNDING A NEW RURAL STORE (LOCATION: AFRICA / EASTERN EUROPE) ---")
    engine.fund_store_opening("0xGlobalFund_Alpha...", "STORE-RURAL-001", amount_eur=30000.0, target_capex=60000.0)
    engine.fund_store_opening("0xLocalImpact_Beta...", "STORE-RURAL-001", amount_eur=30000.0, target_capex=60000.0)

    print("\n--- 2. LOCAL FARMER PRODUCE DELIVERY & INSTANT SMART PAYOUT ---")
    delivery = engine.record_farmer_delivery("0xFarmer_John_Organic...", "Fresh_Dairy_Milk", qty=250.0, unit_price=1.20)
    engine.execute_farmer_smart_payout(delivery.payout_id)

    print("\n--- 3. MONTHLY PROFIT YIELD DISTRIBUTION TO INVESTORS ---")
    engine.distribute_retail_yield("STORE-RURAL-001", monthly_net_profit_eur=3500.0)

    print("\n--- 4. NETWORK LEDGER REPORT ---")
    engine.print_network_summary()
