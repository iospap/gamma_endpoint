import logging
import sys
import asyncio

from decimal import Decimal
from hexbytes import HexBytes
from web3 import Web3

from sources.web3.bins.formulas import univ3_formulas
from sources.web3.bins.w3.objects.basic import web3wrap, erc20


class univ3_pool(web3wrap):
    # SETUP
    def __init__(
        self,
        address: str,
        network: str,
        abi_filename: str = "",
        abi_path: str = "",
        block: int = 0,
        custom_web3: Web3 | None = None,
        custom_web3Url: str | None = None,
    ):
        self._abi_filename = abi_filename or "univ3_pool"
        self._abi_path = abi_path or "sources/common/abis/uniswap/v3"

        self._token0: erc20 = None
        self._token1: erc20 = None

        super().__init__(
            address=address,
            network=network,
            abi_filename=self._abi_filename,
            abi_path=self._abi_path,
            block=block,
            custom_web3=custom_web3,
            custom_web3Url=custom_web3Url,
        )

    # PROPERTIES
    @property
    async def factory(self) -> str:
        return await self._contract.functions.factory().call(
            block_identifier=self.block
        )

    @property
    async def fee(self) -> int:
        """The pool's fee in hundredths of a bip, i.e. 1e-6"""
        return await self._contract.functions.fee().call(block_identifier=self.block)

    @property
    async def feeGrowthGlobal0X128(self) -> int:
        """The fee growth as a Q128.128 fees of token0 collected per unit of liquidity for the entire life of the pool
        Returns:
           int: as Q128.128 fees of token0
        """
        return await self._contract.functions.feeGrowthGlobal0X128().call(
            block_identifier=self.block
        )

    @property
    async def feeGrowthGlobal1X128(self) -> int:
        """The fee growth as a Q128.128 fees of token1 collected per unit of liquidity for the entire life of the pool
        Returns:
           int: as Q128.128 fees of token1
        """
        return await self._contract.functions.feeGrowthGlobal1X128().call(
            block_identifier=self.block
        )

    @property
    async def liquidity(self) -> int:
        return await self._contract.functions.liquidity().call(
            block_identifier=self.block
        )

    @property
    async def maxLiquidityPerTick(self) -> int:
        return await self._contract.functions.maxLiquidityPerTick().call(
            block_identifier=self.block
        )

    async def observations(self, input: int):
        return await self._contract.functions.observations(input).call(
            block_identifier=self.block
        )

    async def observe(self, secondsAgo: int):
        """observe _summary_

        Args:
           secondsAgo (int): _description_

        Returns:
           _type_: tickCumulatives   int56[] :  12731930095582
                   secondsPerLiquidityCumulativeX128s   uint160[] :  242821134689165142944235398318169

        """
        return await self._contract.functions.observe(secondsAgo).call(
            block_identifier=self.block
        )

    async def positions(self, position_key: str) -> dict:
        """

        Args:
           position_key (str): 0x....

        Returns:
           _type_:
                   liquidity   uint128 :  99225286851746
                   feeGrowthInside0LastX128   uint256 :  0
                   feeGrowthInside1LastX128   uint256 :  0
                   tokensOwed0   uint128 :  0
                   tokensOwed1   uint128 :  0
        """
        result = await self._contract.functions.positions(position_key).call(
            block_identifier=self.block
        )
        return {
            "liquidity": result[0],
            "feeGrowthInside0LastX128": result[1],
            "feeGrowthInside1LastX128": result[2],
            "tokensOwed0": result[3],
            "tokensOwed1": result[4],
        }

    @property
    async def protocolFees(self) -> list[int]:
        """
        Returns:
           list: [0,0]

        """
        return await self._contract.functions.protocolFees().call(
            block_identifier=self.block
        )

    @property
    async def slot0(self) -> dict:
        """The 0th storage slot in the pool stores many values, and is exposed as a single method to save gas when accessed externally.

        Returns:
           _type_: sqrtPriceX96   uint160 :  28854610805518743926885543006518067
                   tick   int24 :  256121
                   observationIndex   uint16 :  198
                   observationCardinality   uint16 :  300
                   observationCardinalityNext   uint16 :  300
                   feeProtocol   uint8 :  0
                   unlocked   bool :  true
        """
        tmp = await self._contract.functions.slot0().call(block_identifier=self.block)
        return {
            "sqrtPriceX96": tmp[0],
            "tick": tmp[1],
            "observationIndex": tmp[2],
            "observationCardinality": tmp[3],
            "observationCardinalityNext": tmp[4],
            "feeProtocol": tmp[5],
            "unlocked": tmp[6],
        }

    async def snapshotCumulativeInside(self, tickLower: int, tickUpper: int):
        return await self._contract.functions.snapshotCumulativeInside(
            tickLower, tickUpper
        ).call(block_identifier=self.block)

    async def tickBitmap(self, input: int) -> int:
        return await self._contract.functions.tickBitmap(input).call(
            block_identifier=self.block
        )

    @property
    async def tickSpacing(self) -> int:
        return await self._contract.functions.tickSpacing().call(
            block_identifier=self.block
        )

    async def ticks(self, tick: int) -> dict:
        """

        Args:
           tick (int):

        Returns:
           _type_:     liquidityGross   uint128 :  0
                       liquidityNet   int128 :  0
                       feeGrowthOutside0X128   uint256 :  0
                       feeGrowthOutside1X128   uint256 :  0
                       tickCumulativeOutside   int56 :  0
                       spoolecondsPerLiquidityOutsideX128   uint160 :  0
                       secondsOutside   uint32 :  0
                       initialized   bool :  false
        """
        result = await self._contract.functions.ticks(tick).call(
            block_identifier=self.block
        )
        return {
            "liquidityGross": result[0],
            "liquidityNet": result[1],
            "feeGrowthOutside0X128": result[2],
            "feeGrowthOutside1X128": result[3],
            "tickCumulativeOutside": result[4],
            "secondsPerLiquidityOutsideX128": result[5],
            "secondsOutside": result[6],
            "initialized": result[7],
        }

    @property
    async def token0(self) -> erc20:
        """The first of the two tokens of the pool, sorted by address

        Returns:
        """
        if self._token0 is None:
            self._token0 = erc20(
                address=await self._contract.functions.token0().call(
                    block_identifier=self.block
                ),
                network=self._network,
                block=self.block,
                custom_web3Url=self.w3.provider.endpoint_uri,
            )
        return self._token0

    @property
    async def token1(self) -> erc20:
        """The second of the two tokens of the pool, sorted by address_

        Returns:
           erc20:
        """
        if self._token1 is None:
            self._token1 = erc20(
                address=await self._contract.functions.token1().call(
                    block_identifier=self.block
                ),
                network=self._network,
                block=self.block,
                custom_web3Url=self.w3.provider.endpoint_uri,
            )
        return self._token1

    # write function without state change ( not wrkin)
    async def collect(
        self, recipient, tickLower, tickUpper, amount0Requested, amount1Requested, owner
    ):
        return await self._contract.functions.collect(
            recipient, tickLower, tickUpper, amount0Requested, amount1Requested
        ).call({"from": owner})

    # CUSTOM PROPERTIES
    @property
    def block(self) -> int:
        return self._block

    @block.setter
    def block(self, value: int):
        # set block
        self._block = value
        self.token0.block = value
        self.token1.block = value

    # CUSTOM FUNCTIONS
    async def position(self, ownerAddress: str, tickLower: int, tickUpper: int) -> dict:
        """

        Returns:
           dict:
                   liquidity   uint128 :  99225286851746
                   feeGrowthInside0LastX128   uint256 :  0
                   feeGrowthInside1LastX128   uint256 :  0
                   tokensOwed0   uint128 :  0
                   tokensOwed1   uint128 :  0
        """
        return await self.positions(
            univ3_formulas.get_positionKey(
                ownerAddress=ownerAddress,
                tickLower=tickLower,
                tickUpper=tickUpper,
            )
        )

    async def get_qtty_depoloyed(
        self, ownerAddress: str, tickUpper: int, tickLower: int, inDecimal: bool = True
    ) -> dict:
        """Retrieve the quantity of tokens currently deployed

        Args:
           ownerAddress (str):
           tickUpper (int):
           tickLower (int):
           inDecimal (bool): return result in a decimal format?

        Returns:
           dict: {
                   "qtty_token0":0,        (int or Decimal) # quantity of token 0 deployed in dex
                   "qtty_token1":0,        (int or Decimal) # quantity of token 1 deployed in dex
                   "fees_owed_token0":0,   (int or Decimal) # quantity of token 0 fees owed to the position ( not included in qtty_token0 and this is not uncollected fees)
                   "fees_owed_token1":0,   (int or Decimal) # quantity of token 1 fees owed to the position ( not included in qtty_token1 and this is not uncollected fees)
                 }
        """

        result = {
            "qtty_token0": 0,  # quantity of token 0 deployed in dex
            "qtty_token1": 0,  # quantity of token 1 deployed in dex
            "fees_owed_token0": 0,  # quantity of token 0 fees owed to the position ( not included in qtty_token0 and this is not uncollected fees)
            "fees_owed_token1": 0,  # quantity of token 1 fees owed to the position ( not included in qtty_token1 and this is not uncollected fees)
        }

        # get position and slot data
        pos, slot0 = asyncio.gather(
            self.position(
                ownerAddress=Web3.to_checksum_address(ownerAddress.lower()),
                tickLower=tickLower,
                tickUpper=tickUpper,
            ),
            self.slot0,
        )

        # get current tick from slot
        tickCurrent = slot0["tick"]
        sqrtRatioX96 = slot0["sqrtPriceX96"]
        sqrtRatioAX96 = univ3_formulas.TickMath.getSqrtRatioAtTick(tickLower)
        sqrtRatioBX96 = univ3_formulas.TickMath.getSqrtRatioAtTick(tickUpper)
        # calc quantity from liquidity
        (
            result["qtty_token0"],
            result["qtty_token1"],
        ) = univ3_formulas.LiquidityAmounts.getAmountsForLiquidity(
            sqrtRatioX96, sqrtRatioAX96, sqrtRatioBX96, pos["liquidity"]
        )

        # add owed tokens
        result["fees_owed_token0"] = pos["tokensOwed0"]
        result["fees_owed_token1"] = pos["tokensOwed1"]

        # convert to decimal as needed
        if inDecimal:
            self._get_qtty_depoloyed_todecimal(result)
        # return result
        return result.copy()

    def _get_qtty_depoloyed_todecimal(self, result):
        # get token decimals
        decimals_token0 = self.token0.decimals
        decimals_token1 = self.token1.decimals

        result["qtty_token0"] = Decimal(result["qtty_token0"]) / Decimal(
            10**decimals_token0
        )
        result["qtty_token1"] = Decimal(result["qtty_token1"]) / Decimal(
            10**decimals_token1
        )
        result["fees_owed_token0"] = Decimal(result["fees_owed_token0"]) / Decimal(
            10**decimals_token0
        )
        result["fees_owed_token1"] = Decimal(result["fees_owed_token1"]) / Decimal(
            10**decimals_token1
        )

    async def get_fees_uncollected(
        self, ownerAddress: str, tickUpper: int, tickLower: int, inDecimal: bool = True
    ) -> dict:
        """Retrieve the quantity of fees not collected nor yet owed ( but certain) to the deployed position

        Args:
            ownerAddress (str):
            tickUpper (int):
            tickLower (int):
            inDecimal (bool): return result in a decimal format?

        Returns:
            dict: {
                    "qtty_token0":0,   (int or Decimal)     # quantity of uncollected token 0
                    "qtty_token1":0,   (int or Decimal)     # quantity of uncollected token 1
                }
        """

        result = {
            "qtty_token0": 0,
            "qtty_token1": 0,
        }

        # get position data and ticks
        pos, tickCurrent, ticks_lower, ticks_upper = asyncio.gather(
            self.position(
                ownerAddress=Web3.to_checksum_address(ownerAddress.lower()),
                tickLower=tickLower,
                tickUpper=tickUpper,
            ),
            self.slot0["tick"],
            self.ticks(tickLower),
            self.ticks(tickUpper),
        )

        (
            result["qtty_token0"],
            result["qtty_token1"],
        ) = univ3_formulas.get_uncollected_fees(
            fee_growth_global_0=self.feeGrowthGlobal0X128,
            fee_growth_global_1=self.feeGrowthGlobal1X128,
            tick_current=tickCurrent,
            tick_lower=tickLower,
            tick_upper=tickUpper,
            fee_growth_outside_0_lower=ticks_lower["feeGrowthOutside0X128"],
            fee_growth_outside_1_lower=ticks_lower["feeGrowthOutside1X128"],
            fee_growth_outside_0_upper=ticks_upper["feeGrowthOutside0X128"],
            fee_growth_outside_1_upper=ticks_upper["feeGrowthOutside1X128"],
            liquidity=pos["liquidity"],
            fee_growth_inside_last_0=pos["feeGrowthInside0LastX128"],
            fee_growth_inside_last_1=pos["feeGrowthInside1LastX128"],
        )

        # convert to decimal as needed
        if inDecimal:
            result["qtty_token0"] = Decimal(result["qtty_token0"]) / Decimal(
                10**self.token0.decimals
            )
            result["qtty_token1"] = Decimal(result["qtty_token1"]) / Decimal(
                10**self.token1.decimals
            )

        # return result
        return result.copy()

    async def as_dict(self, convert_bint=False, static_mode: bool = False) -> dict:
        """as_dict _summary_

        Args:
            convert_bint (bool, optional): convert big integers to string . Defaults to False.
            static_mode (bool, optional): return only static pool parameters. Defaults to False.

        Returns:
            dict:
        """
        result = await super().as_dict(convert_bint=convert_bint)

        (
            result["fee"],
            result["tickSpacing"],
            result["token0"],
            result["token1"],
            result["protocolFees"],
        ) = asyncio.gather(
            self.fee,
            self.tickSpacing,
            self.token0.as_dict(convert_bint=convert_bint),
            self.token1.as_dict(convert_bint=convert_bint),
            self.protocolFees,
        )

        # identify pool dex
        result["dex"] = self.identify_dex_name()

        if convert_bint:
            result["tickSpacing"] = str(result["tickSpacing"])
            result["protocolFees"] = [str(i) for i in result["protocolFees"]]

        if not static_mode:
            await self._as_dict_not_static_items(convert_bint, result)
        return result

    async def _as_dict_not_static_items(self, convert_bint, result):
        (
            result["feeGrowthGlobal0X128"],
            result["feeGrowthGlobal1X128"],
            result["liquidity"],
            result["maxLiquidityPerTick"],
            result["slot0"],
        ) = asyncio.gather(
            self.feeGrowthGlobal0X128,
            self.feeGrowthGlobal1X128,
            self.liquidity,
            self.maxLiquidityPerTick,
        )

        # slot0
        result["slot0"] = self.slot0
        if convert_bint:
            result["feeGrowthGlobal0X128"] = str(result["feeGrowthGlobal0X128"])
            result["feeGrowthGlobal1X128"] = str(result["feeGrowthGlobal1X128"])
            result["liquidity"] = str(result["liquidity"])
            result["maxLiquidityPerTick"] = str(result["maxLiquidityPerTick"])
            result["slot0"]["sqrtPriceX96"] = str(result["slot0"]["sqrtPriceX96"])
            result["slot0"]["tick"] = str(result["slot0"]["tick"])
            result["slot0"]["observationIndex"] = str(
                result["slot0"]["observationIndex"]
            )
            result["slot0"]["observationCardinality"] = str(
                result["slot0"]["observationCardinality"]
            )
            result["slot0"]["observationCardinalityNext"] = str(
                result["slot0"]["observationCardinalityNext"]
            )


class algebrav3_dataStorageOperator(web3wrap):
    # SETUP
    def __init__(
        self,
        address: str,
        network: str,
        abi_filename: str = "",
        abi_path: str = "",
        block: int = 0,
        custom_web3: Web3 | None = None,
        custom_web3Url: str | None = None,
    ):
        self._abi_filename = abi_filename or "dataStorageOperator"
        self._abi_path = abi_path or "sources/common/abis/algebra/v3"

        super().__init__(
            address=address,
            network=network,
            abi_filename=self._abi_filename,
            abi_path=self._abi_path,
            block=block,
            custom_web3=custom_web3,
            custom_web3Url=custom_web3Url,
        )

    # TODO: Implement contract functs calculateVolumePerLiquidity, getAverages, getFee, getSingleTimepoint, getTimepoints and timepoints

    @property
    async def feeConfig(self) -> dict:
        """feeConfig _summary_

        Returns:
            dict:   { alpha1   uint16 :  100
                        alpha2   uint16 :  3600
                        beta1   uint32 :  500
                        beta2   uint32 :  80000
                        gamma1   uint16 :  80
                        gamma2   uint16 :  11750
                        volumeBeta   uint32 :  0
                        volumeGamma   uint16 :  10
                        baseFee   uint16 :  400 }

        """
        return await self._contract.functions.feeConfig().call(
            block_identifier=self.block
        )

    @property
    async def window(self) -> int:
        """window _summary_

        Returns:
            int: 86400 uint32
        """
        return await self._contract.functions.window().call(block_identifier=self.block)


class algebrav3_pool(web3wrap):
    # SETUP
    def __init__(
        self,
        address: str,
        network: str,
        abi_filename: str = "",
        abi_path: str = "",
        block: int = 0,
        custom_web3: Web3 | None = None,
        custom_web3Url: str | None = None,
    ):
        self._abi_filename = abi_filename or "algebrav3pool"
        self._abi_path = abi_path or "sources/common/abis/algebra/v3"

        self._token0: erc20 = None
        self._token1: erc20 = None

        self._dataStorage: algebrav3_dataStorageOperator = None

        super().__init__(
            address=address,
            network=network,
            abi_filename=self._abi_filename,
            abi_path=self._abi_path,
            block=block,
            custom_web3=custom_web3,
            custom_web3Url=custom_web3Url,
        )

    # PROPERTIES

    @property
    async def activeIncentive(self) -> str:
        """activeIncentive

        Returns:
            str: address
        """
        return await self._contract.functions.activeIncentive().call(
            block_identifier=self.block
        )

    @property
    async def dataStorageOperator(self) -> algebrav3_dataStorageOperator:
        """ """
        if self._dataStorage is None:
            self._dataStorage = algebrav3_dataStorageOperator(
                address=await self._contract.functions.dataStorageOperator().call(
                    block_identifier=self.block
                ),
                network=self._network,
                block=self.block,
                custom_web3Url=self.w3.provider.endpoint_uri,
            )
        return self._dataStorage

    @property
    async def factory(self) -> str:
        return await self._contract.functions.factory().call(
            block_identifier=self.block
        )

    @property
    async def getInnerCumulatives(self, bottomTick: int, topTick: int) -> dict:
        return await self._contract.functions.getInnerCumulatives(
            bottomTick, topTick
        ).call(block_identifier=self.block)

    @property
    async def getTimepoints(self, secondsAgo: int) -> dict:
        return await self._contract.functions.getTimepoints(secondsAgo).call(
            block_identifier=self.block
        )

    @property
    async def globalState(self) -> dict:
        """

        Returns:
           dict:   sqrtPriceX96  uint160 :  28854610805518743926885543006518067  ( <price> at contract level)
                   tick   int24 :  256121
                   fee   uint16 :  198
                   timepointIndex   uint16 :  300
                   communityFeeToken0   uint8 :  300
                   communityFeeToken1   uint8 :  0
                   unlocked   bool :  true
        """
        tmp = await self._contract.functions.globalState().call(
            block_identifier=self.block
        )
        return {
            "sqrtPriceX96": tmp[0],
            "tick": tmp[1],
            "fee": tmp[2],
            "timepointIndex": tmp[3],
            "communityFeeToken0": tmp[4],
            "communityFeeToken1": tmp[5],
            "unlocked": tmp[6],
        }

    @property
    async def liquidity(self) -> int:
        """liquidity _summary_

        Returns:
            int: 14468296980040792163 uint128
        """
        return await self._contract.functions.liquidity().call(
            block_identifier=self.block
        )

    @property
    async def liquidityCooldown(self) -> int:
        """liquidityCooldown _summary_

        Returns:
            int: 0 uint32
        """
        return await self._contract.functions.liquidityCooldown().call(
            block_identifier=self.block
        )

    @property
    async def maxLiquidityPerTick(self) -> int:
        """maxLiquidityPerTick _summary_

        Returns:
            int: 11505743598341114571880798222544994 uint128
        """
        return await self._contract.functions.maxLiquidityPerTick().call(
            block_identifier=self.block
        )

    async def positions(self, position_key: str) -> dict:
        """

        Args:
           position_key (str): 0x....

        Returns:
           _type_:
                   liquidity   uint128 :  99225286851746
                   lastLiquidityAddTimestamp
                   innerFeeGrowth0Token   uint256 :  (feeGrowthInside0LastX128)
                   innerFeeGrowth1Token   uint256 :  (feeGrowthInside1LastX128)
                   fees0   uint128 :  0  (tokensOwed0)
                   fees1   uint128 :  0  ( tokensOwed1)
        """

        result = await self._contract.functions.positions(HexBytes(position_key)).call(
            block_identifier=self.block
        )
        return {
            "liquidity": result[0],
            "lastLiquidityAddTimestamp": result[1],
            "feeGrowthInside0LastX128": result[2],
            "feeGrowthInside1LastX128": result[3],
            "tokensOwed0": result[4],
            "tokensOwed1": result[5],
        }

    @property
    async def tickSpacing(self) -> int:
        """tickSpacing _summary_

        Returns:
            int: 60 int24
        """
        return await self._contract.functions.tickSpacing().call(
            block_identifier=self.block
        )

    async def tickTable(self, value: int) -> int:
        return await self._contract.functions.tickTable(value).call(
            block_identifier=self.block
        )

    async def ticks(self, tick: int) -> dict:
        """

        Args:
           tick (int):

        Returns:
           _type_:     liquidityGross   uint128 :  0        liquidityTotal
                       liquidityNet   int128 :  0           liquidityDelta
                       feeGrowthOutside0X128   uint256 :  0 outerFeeGrowth0Token
                       feeGrowthOutside1X128   uint256 :  0 outerFeeGrowth1Token
                       tickCumulativeOutside   int56 :  0   outerTickCumulative
                       spoolecondsPerLiquidityOutsideX128   uint160 :  0    outerSecondsPerLiquidity
                       secondsOutside   uint32 :  0         outerSecondsSpent
                       initialized   bool :  false          initialized
        """
        result = await self._contract.functions.ticks(tick).call(
            block_identifier=self.block
        )
        return {
            "liquidityGross": result[0],
            "liquidityNet": result[1],
            "feeGrowthOutside0X128": result[2],
            "feeGrowthOutside1X128": result[3],
            "tickCumulativeOutside": result[4],
            "secondsPerLiquidityOutsideX128": result[5],
            "secondsOutside": result[6],
            "initialized": result[7],
        }

    async def timepoints(self, index: int) -> dict:
        #   initialized bool, blockTimestamp uint32, tickCumulative int56, secondsPerLiquidityCumulative uint160, volatilityCumulative uint88, averageTick int24, volumePerLiquidityCumulative uint144
        return await self._contract.functions.timepoints(index).call(
            block_identifier=self.block
        )

    @property
    async def token0(self) -> erc20:
        """The first of the two tokens of the pool, sorted by address

        Returns:
           erc20:
        """
        if self._token0 is None:
            self._token0 = erc20(
                address=await self._contract.functions.token0().call(
                    block_identifier=self.block
                ),
                network=self._network,
                block=self.block,
                custom_web3Url=self.w3.provider.endpoint_uri,
            )
        return self._token0

    @property
    async def token1(self) -> erc20:
        if self._token1 is None:
            self._token1 = erc20(
                address=await self._contract.functions.token1().call(
                    block_identifier=self.block
                ),
                network=self._network,
                block=self.block,
                custom_web3Url=self.w3.provider.endpoint_uri,
            )
        return self._token1

    @property
    async def feeGrowthGlobal0X128(self) -> int:
        """The fee growth as a Q128.128 fees of token0 collected per unit of liquidity for the entire life of the pool
        Returns:
           int: as Q128.128 fees of token0
        """
        return await self._contract.functions.totalFeeGrowth0Token().call(
            block_identifier=self.block
        )

    @property
    async def feeGrowthGlobal1X128(self) -> int:
        """The fee growth as a Q128.128 fees of token1 collected per unit of liquidity for the entire life of the pool
        Returns:
           int: as Q128.128 fees of token1
        """
        return await self._contract.functions.totalFeeGrowth1Token().call(
            block_identifier=self.block
        )

    # CUSTOM PROPERTIES
    @property
    def block(self) -> int:
        return self._block

    @block.setter
    def block(self, value: int):
        # set block
        self._block = value
        self.token0.block = value
        self.token1.block = value

    # CUSTOM FUNCTIONS
    async def position(self, ownerAddress: str, tickLower: int, tickUpper: int) -> dict:
        """

        Returns:
           dict:
                   liquidity   uint128 :  99225286851746
                   feeGrowthInside0LastX128   uint256 :  0
                   feeGrowthInside1LastX128   uint256 :  0
                   tokensOwed0   uint128 :  0
                   tokensOwed1   uint128 :  0
        """
        return await self.positions(
            univ3_formulas.get_positionKey_algebra(
                ownerAddress=ownerAddress,
                tickLower=tickLower,
                tickUpper=tickUpper,
            )
        )

    async def get_qtty_depoloyed(
        self, ownerAddress: str, tickUpper: int, tickLower: int, inDecimal: bool = True
    ) -> dict:
        """Retrieve the quantity of tokens currently deployed

        Args:
           ownerAddress (str):
           tickUpper (int):
           tickLower (int):
           inDecimal (bool): return result in a decimal format?

        Returns:
           dict: {
                   "qtty_token0":0,        (int or Decimal) # quantity of token 0 deployed in dex
                   "qtty_token1":0,        (int or Decimal) # quantity of token 1 deployed in dex
                   "fees_owed_token0":0,   (int or Decimal) # quantity of token 0 fees owed to the position ( not included in qtty_token0 and this is not uncollected fees)
                   "fees_owed_token1":0,   (int or Decimal) # quantity of token 1 fees owed to the position ( not included in qtty_token1 and this is not uncollected fees)
                 }
        """

        result = {
            "qtty_token0": 0,  # quantity of token 0 deployed in dex
            "qtty_token1": 0,  # quantity of token 1 deployed in dex
            "fees_owed_token0": 0,  # quantity of token 0 fees owed to the position ( not included in qtty_token0 and this is not uncollected fees)
            "fees_owed_token1": 0,  # quantity of token 1 fees owed to the position ( not included in qtty_token1 and this is not uncollected fees)
        }

        # get position and slot data
        pos, slot0 = await asyncio.gather(
            self.position(
                ownerAddress=Web3.to_checksum_address(ownerAddress.lower()),
                tickLower=tickLower,
                tickUpper=tickUpper,
            ),
            self.globalState,
        )

        # get current tick from slot
        tickCurrent = slot0["tick"]
        sqrtRatioX96 = slot0["sqrtPriceX96"]
        sqrtRatioAX96 = univ3_formulas.TickMath.getSqrtRatioAtTick(tickLower)
        sqrtRatioBX96 = univ3_formulas.TickMath.getSqrtRatioAtTick(tickUpper)
        # calc quantity from liquidity
        (
            result["qtty_token0"],
            result["qtty_token1"],
        ) = univ3_formulas.LiquidityAmounts.getAmountsForLiquidity(
            sqrtRatioX96, sqrtRatioAX96, sqrtRatioBX96, pos["liquidity"]
        )

        # add owed tokens
        result["fees_owed_token0"] = pos["tokensOwed0"]
        result["fees_owed_token1"] = pos["tokensOwed1"]

        # convert to decimal as needed
        if inDecimal:
            await self._get_qtty_depoloyed_todecimal(result)
        # return result
        return result.copy()

    async def _get_qtty_depoloyed_todecimal(self, result):
        # get token decimals
        decimals_token0, decimals_token1 = asyncio.gather(
            self.token0.decimals, self.token1.decimals
        )

        result["qtty_token0"] = Decimal(result["qtty_token0"]) / Decimal(
            10**decimals_token0
        )
        result["qtty_token1"] = Decimal(result["qtty_token1"]) / Decimal(
            10**decimals_token1
        )
        result["fees_owed_token0"] = Decimal(result["fees_owed_token0"]) / Decimal(
            10**decimals_token0
        )
        result["fees_owed_token1"] = Decimal(result["fees_owed_token1"]) / Decimal(
            10**decimals_token1
        )

    async def get_fees_uncollected(
        self, ownerAddress: str, tickUpper: int, tickLower: int, inDecimal: bool = True
    ) -> dict:
        """Retrieve the quantity of fees not collected nor yet owed ( but certain) to the deployed position

        Args:
            ownerAddress (str):
            tickUpper (int):
            tickLower (int):
            inDecimal (bool): return result in a decimal format?

        Returns:
            dict: {
                    "qtty_token0":0,   (int or Decimal)     # quantity of uncollected token 0
                    "qtty_token1":0,   (int or Decimal)     # quantity of uncollected token 1
                }
        """

        result = {
            "qtty_token0": 0,
            "qtty_token1": 0,
        }

        # get position and ticks data
        pos, tickCurrent, ticks_lower, ticks_upper = await asyncio.gather(
            self.position(
                ownerAddress=Web3.to_checksum_address(ownerAddress.lower()),
                tickLower=tickLower,
                tickUpper=tickUpper,
            ),
            self.globalState["tick"],
            self.ticks(tickLower),
            self.ticks(tickUpper),
        )

        (
            result["qtty_token0"],
            result["qtty_token1"],
        ) = univ3_formulas.get_uncollected_fees(
            fee_growth_global_0=self.feeGrowthGlobal0X128,
            fee_growth_global_1=self.feeGrowthGlobal1X128,
            tick_current=tickCurrent,
            tick_lower=tickLower,
            tick_upper=tickUpper,
            fee_growth_outside_0_lower=ticks_lower["feeGrowthOutside0X128"],
            fee_growth_outside_1_lower=ticks_lower["feeGrowthOutside1X128"],
            fee_growth_outside_0_upper=ticks_upper["feeGrowthOutside0X128"],
            fee_growth_outside_1_upper=ticks_upper["feeGrowthOutside1X128"],
            liquidity=pos["liquidity"],
            fee_growth_inside_last_0=pos["feeGrowthInside0LastX128"],
            fee_growth_inside_last_1=pos["feeGrowthInside1LastX128"],
        )

        # convert to decimal as needed
        if inDecimal:
            # get token decimals
            decimals_token0, decimals_token1 = asyncio.gather(
                self.token0.decimals, self.token1.decimals
            )

            result["qtty_token0"] = Decimal(result["qtty_token0"]) / Decimal(
                10**decimals_token0
            )
            result["qtty_token1"] = Decimal(result["qtty_token1"]) / Decimal(
                10**decimals_token1
            )

        # return result
        return result.copy()

    async def as_dict(self, convert_bint=False, static_mode: bool = False) -> dict:
        """as_dict _summary_

        Args:
            convert_bint (bool, optional): convert big integers to string. Defaults to False.
            static_mode (bool, optional): return  static fields only. Defaults to False.

        Returns:
            dict:
        """

        result = await super().as_dict(convert_bint=convert_bint)

        (
            result["activeIncentive"],
            result["liquidityCooldown"],
            result["maxLiquidityPerTick"],
            result["fee"],
            result["token0"],
            result["token1"],
        ) = asyncio.gather(
            self.activeIncentive,
            self.liquidityCooldown,
            self.maxLiquidityPerTick,
            self.globalState["fee"],
            self.token0.as_dict(convert_bint=convert_bint),
            self.token1.as_dict(convert_bint=convert_bint),
        )

        if convert_bint:
            result["liquidityCooldown"] = str(result["liquidityCooldown"])
            result["maxLiquidityPerTick"] = str(result["maxLiquidityPerTick"])

        # t spacing
        # result["tickSpacing"] = (
        #     self.tickSpacing if not convert_bint else str(self.tickSpacing)
        # )

        # identify pool dex
        result["dex"] = self.identify_dex_name()

        if not static_mode:
            (
                result["feeGrowthGlobal0X128"],
                result["feeGrowthGlobal1X128"],
                result["liquidity"],
                result["globalState"],
            ) = asyncio.gather(
                self.feeGrowthGlobal0X128,
                self.feeGrowthGlobal1X128,
                self.liquidity,
                self.globalState,
            )

            if convert_bint:
                result["feeGrowthGlobal0X128"] = str(result["feeGrowthGlobal0X128"])
                result["feeGrowthGlobal1X128"] = str(result["feeGrowthGlobal1X128"])
                result["liquidity"] = str(result["liquidity"])

                try:
                    result["globalState"]["sqrtPriceX96"] = (
                        str(result["globalState"]["sqrtPriceX96"])
                        if "sqrtPriceX96" in result["globalState"]
                        else ""
                    )
                    # result["globalState"]["price"] = (
                    #     str(result["globalState"]["price"])
                    #     if "price" in result["globalState"]
                    #     else ""
                    # )
                    result["globalState"]["tick"] = (
                        str(result["globalState"]["tick"])
                        if "tick" in result["globalState"]
                        else ""
                    )
                    result["globalState"]["fee"] = (
                        str(result["globalState"]["fee"])
                        if "fee" in result["globalState"]
                        else ""
                    )
                    result["globalState"]["timepointIndex"] = (
                        str(result["globalState"]["timepointIndex"])
                        if "timepointIndex" in result["globalState"]
                        else ""
                    )
                except Exception:
                    logging.getLogger(__name__).warning(
                        f' Unexpected error converting globalState of {result["address"]} at block {result["block"]}     error-> {sys.exc_info()[0]}   globalState: {result["globalState"]}'
                    )

        return result
