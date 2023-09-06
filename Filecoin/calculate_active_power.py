#  一个扇区的有效算力`QualityAdjustedPower` = 扇区大小`sectorSize` * 质量乘积`quality`。
# $$quality=((sectorSize * duration - (DealWeight + VerifiedDealWeight)) * 10 + DealWeight * 10 + VerifiedDealWeight * 100) / ( sectorSize   * duration) / 10 $$
# duration为扇区持续时间，即sector.`Expiration` - sector.`Activation`。
# 从上述公式能看出，只有`VerifiedDealWeight`才有10倍乘积。
#




#
# 没有， dealspace只是用来和sectorsize比较
# 某个deal的dealweight=deal持续时间 * PieceSize （verified deal和非verified deal都是这么算的）
# 扇区的DealWeight = 非verified deal 的dealweight之和，扇区的VerifiedDealWeight = verified deal 的dealweight之和
# sector有效算力 = sectorsize * quality
# quality = ( (sectorsize*扇区生命周期-(DealWeight + VerifiedDealWeight))*10  +  DealWeight*10  +  VerifiedDealWeight*100 )  /  (sectorsize*扇区生命周期)  /  10


sectorSize = 32*1024*1024*1024
duration = 272203-3402656
VerifiedDealWeight = 0
DealWeight = 632040316297498

quality = ((sectorSize * duration - (DealWeight + VerifiedDealWeight)) * 10 + DealWeight * 10 + VerifiedDealWeight * 100) / ( sectorSize   * duration) / 10

QualityAdjustedPower = sectorSize * quality

print(QualityAdjustedPower/1024/1024/1024)


