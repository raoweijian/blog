生物信息上的东西，由于发展的时间不长，所以各种标准都不算是广泛传播。
尤其是文件格式之类的，中文版的资料很少，不少英文版的说明也不是很清晰。
这里对SAM格式进行一下解释，希望对新人有所帮助。

如下是SAM文件中的一行
```
FCC0YG3ACXX:2:1103:1572:139769#GCTTAATG	99	chr10	60001	0	90M	=	60390	479	GAATTCCTTGAGGCCTAAATGCATCGGGGTGCTCTGGTTTTGTTGTTGTTATTTCTGAATGACATTTACTTTGGTGCTCTTTATTTTGCG	CCCFFFFFHHHHHJJJJJJJJIJJJJJJJ?HHGIJJJBFHIJIJIDHIHIEHJJIJJIJJJHHGHHHFFFFFFEDCEEECCDDDDEECDD	XT:A:R	NM:i:0	SM:i:0	AM:i:0	X0:i:2	X1:i:0	XM:i:0	XO:i:0	XG:i:0	MD:Z:90	XA:Z:chr18,+14415,90M,0;	RG:Z:120618_I245_FCC0YG3ACXX_L2_SZAXPI010030-30
```
一共12列，每一列含义如下：
1. read的名字，也就是ID（如果是双短测序的话，则同一个ID会有两条reads）
2. flag，为各个标志的和，下面会有详细说明
3. 比对到的染色体号
4. 第一个比对上的碱基所在位置
5. 质量值
6. CIGAR，下面会有详细说明
7. mate比对上的染色体号，如果是“=”，则表示在同一条染色体上
8. mate第一个比对上的碱基所在位置
9. 该read和mate的距离
10. 序列
11. 序列对应的质量值
12. 标记


##CIGAR含义解释
一个稍复杂的CIGAR例子：
```
4S153M1D132M1D5M1D28M1D73M3I12M1I40M54S
```
S表示 solf clip, 4S就表示4个碱基没有比对上
M表示 match 或者 mismatch 153M表示连续153个碱基都比对上了。
　为什么会有
