import json
import os
# import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

class StatsManager:
    def __init__(self, data_file="data/trade_history.json"):
        self.data_file = data_file
        if not os.path.exists("data"):
            os.makedirs("data")
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []

    def save_trade(self, symbol, side, entry_price, exit_price, pnl_pct, pnl_usd, order_id=None):
        trade = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl_pct": pnl_pct,
            "pnl_usd": pnl_usd,
            "order_id": order_id
        }
        self.history.append(trade)
        with open(self.data_file, "w") as f:
            json.dump(self.history, f, indent=4)

    def get_stats(self, period="day"):
        now = datetime.utcnow()
        if period == "day":
            filtered = [t for t in self.history if (now - datetime.fromisoformat(t['timestamp'])).days < 1]
        elif period == "week":
            filtered = [t for t in self.history if (now - datetime.fromisoformat(t['timestamp'])).days < 7]
        else: # month
            filtered = [t for t in self.history if (now - datetime.fromisoformat(t['timestamp'])).days < 30]

        if not filtered:
            return {"win_rate": 0, "pnl": 0.0, "count": 0, "max_dd": 0.0}

        wins = len([t for t in filtered if t['pnl_usd'] > 0])
        pnl = sum([t['pnl_usd'] for t in filtered])
        
        # Simple Drawdown calculation based on history
        cumulative_pnl = 0
        peak = 0
        max_dd = 0
        for t in filtered:
            cumulative_pnl += t['pnl_usd']
            if cumulative_pnl > peak:
                peak = cumulative_pnl
            dd = peak - cumulative_pnl
            if dd > max_dd:
                max_dd = dd

        return {
            "win_rate": int((wins / len(filtered)) * 100),
            "pnl": pnl,
            "count": len(filtered),
            "max_dd": round(max_dd, 2)
        }

    def generate_performance_chart(self, output_path="reports/performance.png"):
        return None
        # if not self.history:
        #     return None
        # 
        # df = pd.DataFrame(self.history)
        # df['pnl_cum'] = df['pnl_usd'].cumsum()
        # 
        # plt.figure(figsize=(10, 6))
        # plt.plot(df['pnl_cum'], marker='o', linestyle='-', color='b')
        # plt.title('Rendimiento bit-ia-nuevo v3.0')
        # plt.xlabel('Número de Operación')
        # plt.ylabel('PnL Acumulado (USDT)')
        # plt.grid(True)
        # plt.savefig(output_path)
        # plt.close()
        # return output_path
