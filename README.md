# IART Project #1 - Neutron board game in Python (using Minimax algorithm)

## Heuristic

1000 + 10 * NumEmptyTilesPlayer - 10 * NumEmptyTilesOpponent + 200 * NeutronNumPathsToPlayer - 200 * NeutronNumPathsToOpponent + 10 * Odd * (8 - NumEmptyTilesAroundNeutron) + 500 * VictoryPlayer - 500 * VictoryOpponent

* *NumEmptyTilesPlayer* - Number of empty tiles in the current player's base
* *NumEmptyTilesOpponent* - Number of empty tiles in the opponent's base
* *NeutronNumPathsToPlayer* - Number of paths the Neutron can take directly to the current player's base
* *NeutronNumPathsToOpponent* - Number of paths the Neutron can take directly to the opponents's base
* *NumEmptyTilesAroundNeutron* - Number of empty tiles around Neutron
* *Odd* - **1** *if* *NumEmptyTilesAroundNeutron* is odd *else* **-1**
* *VictoryPlayer* - **1** *if* Neutron is in current player's base *else* **0**
* *VictoryOpponent* - **1** *if* Neutron is in opponent's base *else* **0**
