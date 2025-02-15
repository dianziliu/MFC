<h1 align="center">
A Multi-Factor Collaborative Prediction for Review-based Recommendation
</h1>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="">Paper</a> •
  <a href="#citation">Citation</a>
</p>



Repo for submation of Neural Networks : [A Multi-Factor Collaborative Prediction for Review-based Recommendation]

<h2 id="introduction">1. Introduction✨</h2>

In recommender systems, user behaviors contain clicks, ratings, and reviews. Existing review-based methods implicitly model click behaviors to achieve accurate predictions on rating prediction tasks (RP). However, they ignore the help of the rating behaviors for the click-through rate prediction task (CTR). Although the process from clicks to ratings is generally considered to be one-way, we can still get some information about clicks from ratings. In this paper, we propose a multi-factor collaborative prediction method (MFC) for the review-based recommendation. It mines the complex relationship between click and rating behaviors, achieving accurate prediction on CTR tasks. Specifically, we factorize the complex relationship into three simple relationships, i.e., linear, sharing, and cross-correlation relationships. Thus, we first extract click factors, rating factors, and their sharing factor, from user click and rating behaviors. Then, we design a rating factor regularization method to learn rating factors accurately, helping to model the true relationships between click and rating behavior. Finally, we combine these three factors to make predictions, while click and rating factors are used to model the linear and cross-correlation relationships, while the sharing factors correspond to the sharing relation. Experiments on five real-world datasets demonstrate that MFC outperforms the best baseline by 9.19%, 9.80%, 0.69%, and 7.95%, in terms of Accuracy, Precision, Recall, and F1-score respectively.


<h2 id="quick-start">2. Quick Start🚀</h2>

1. File Structure

```
.\data [training data]  
.\src  
.\untils
```


2. training the model

```sh
python src/main.py
```



<h2 id="citation">3. Citation☕️</h2>

If you find this repository helpful, please consider citing our paper when it has been accepted.

<!-- ```
@inproceedings{liu-ickm-2023-tse,
  author       = {Zhen Yang and
                  Junrui Liu and
                  Tong Li and
                  Di Wu and
                  Shiqiu Yang and
                  Huan Liu},
  editor       = {Ingo Frommholz and
                  Frank Hopfgartner and
                  Mark Lee and
                  Michael Oakes and
                  Mounia Lalmas and
                  Min Zhang and
                  Rodrygo L. T. Santos},
  title        = {A Two-tier Shared Embedding Method for Review-based Recommender Systems},
  booktitle    = {Proceedings of the 32nd {ACM} International Conference on Information
                  and Knowledge Management, {CIKM} 2023, Birmingham, United Kingdom,
                  October 21-25, 2023},
  pages        = {2928--2938},
  publisher    = {{ACM}},
  year         = {2023},
  url          = {https://doi.org/10.1145/3583780.3614770},
  doi          = {10.1145/3583780.3614770},
  timestamp    = {Wed, 22 Nov 2023 13:37:55 +0100},
}
``` -->
