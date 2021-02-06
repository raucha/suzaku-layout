# suzaku-layout
キーボード配列

## 概要
+ Phonenix配列
+ きゅうり配列
の間の子。

## 特徴
+ 拗音も含めて、2打入力可能
+ 右の順番が入れ替わっても訂正可能

---
## 配置最適化

### 環境構築
```
sudo pip3 install pipenv
bash scripts/install_apt_pkg.sh
```

### スクリプト確認
```
cd scripts
pipenv run python -m unittest discover tests
pipenv run python layout_optimizer/layout_optimizer.py   # データセットの文字を打ち込んだときの所要時間を算出
```



### メモ
#### よく使う並びが1
あい 1
あう 1
あえ 1
あお 0

いあ 0
いう 0
いえ 0
いお 0

うあ 0
うい 0
うえ 0
うお 0

えあ 0
えい 1
えう 0
えお 0

おあ 0
おい 1
おう 1
おえ 0

えおうあい
