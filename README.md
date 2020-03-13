# IART Project #1 - Neutron board game in Python (using Minimax algorithm)

## Heuristic

1000 + 10 * NumEmptyTilesPlayer - 10 * NumEmptyTilesOpponent + 200 * NeutronToPlayer - 200 * NeutronToOpponent + 10 * Odd * (8 - NumEmptyTilesAroundNeutron) + 500 * VictoryPlayer - 500 * VictoryOpponent

* *NumEmptyTilesPlayer* - Number of empty tiles in the current player's base
* *NumEmptyTilesOpponent* - Number of empty tiles in the opponent's base
* *NeutronToPlayer* - **1** *if* the Neutron is one move away from being in the current player's base *else* **0**
* *NeutronToOpponent* - **1** *if* the Neutron is one move away from being in the opponent's base *else* **0**
* *NumEmptyTilesAroundNeutron* - Number of empty tiles around Neutron
* *Odd* - **1** *if* *NumEmptyTilesAroundNeutron* is odd *else* **-1**
* *VictoryPlayer* - **1** *if* Neutron is in current player's base *else* **0**
* *VictoryOpponent* - **1** *if* Neutron is in opponent's base *else* **0**
