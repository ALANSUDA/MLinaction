MLinaction
==========

《机器学习实践》的代码，包含了大量修改

本代码库是个人学习《Machine Learning in Action》一书过程中，根据书本代码和scikit-learn library的demo编写的
，基本上涵盖了原生代码和基于scikit代码。
目前涵盖范围：
```javascript
分类功能：
    KNN分类;
    Decision Tree分类;
    Bayersian分类;
    Logistic回归分类;
    SVM支持向量机分类;
    AdaBoost分类;
聚类功能：
    KMeans聚类
文本功能：
    LSA（LSI）主题模型
    pLSA主题模型
    Recommend推荐系统（基于物品的推荐）
信息检索功能：
    新浪微博信息
    百度地图信息检索
```

```javascript
hmgis/
    TextMining/
        /parseFile
            /parseCSV   将从微博数据中获得的CSV文件转化为分词后的文件
    Classifier/         分类器包
        /KNN
            /KNNDemo    KNN分类
                /createDataSet  加载一个内部数据集
                /classify0      分类器
                /file2matrix    将tab文件转化为矩阵
                /show2DTest     数据2D可视化
                /show3DTest     数据3D可视化
                /knnTest        最简单的分类器，测试单个值分类
                /autoNorm       数据归一化，是进行可视化前的必要程序
                /knnTest2       将数据文件中的数据进行分类
                /knnTestScikit  SCIKIT的KNN例子
                /img2vector     影像转化为矩阵
                /handwritingClassTest   影像矩阵的分类
        /DecisionTree
            /DecisionTreeDemo
                /createDataset  将标称数据转化为数值数据矩阵
                /dtTest         使用scikit的DT例子
        /Bayesian
            /Bayesian
            /RSSBayesian
            /EmailClassifier
```