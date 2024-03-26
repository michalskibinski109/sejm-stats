# Sejm stats

<img src="src/sejm_app/static/img/logo.png" alt="sejm-stats" width="200"/>

## [Dokumentacja w języku polskim](https://michalskibinski109.github.io/sejm-stats-docs/)

Welcome to Sejm 2.0, a project aimed at making parliamentary data more accessible and understandable. This project provides a clear and concise view of complex parliamentary data, making it easier for citizens to stay informed about the actions and decisions of their representatives.


## Nowa wersja

![image](https://github.com/michalskibinski109/sejm-stats/assets/77834536/9fe175ed-93f3-44d7-9014-1dae63e8a716)
![Uploading image.png…]()


![image](https://github.com/michalskibinski109/sejm2.0/assets/77834536/51c4e1d1-a340-4b9e-a312-4cdccc52989a)
![image](https://github.com/michalskibinski109/sejm-stats/assets/77834536/dc098f3b-983a-49c5-9fa9-21556b1ff328)

![image](https://github.com/michalskibinski109/sejm2.0/assets/77834536/a1af2d65-eeb9-4110-882f-b701931c6914)
![image](https://github.com/michalskibinski109/sejm2.0/assets/77834536/debd73b5-1dab-4002-82f4-f98c9f400ed6)


## Motivation

The main motivation behind sejm-stats is to make parliamentary information more accessible to everyone. The project is not driven by financial motives, but rather by the desire to keep everyone informed about what's happening in the country. sejm-stats is not affiliated with any political party. The goal is to provide objective and convenient information to help citizens understand the decision-making processes in our country. However, as the project developed, it became clear that some form of financing would be necessary to keep it going.

## Features
Sejm 2.0 is a web app that makes it easy to track the activities of the Polish parliament (Sejm) and its members. It offers a more intuitive and user-friendly interface than the official Sejm website, as well as a number of additional features, including:
- Detailed information about each member of parliament (MP), including their contact information, voting record, and committee assignments.
- A powerful search engine that allows you to find information about specific bills, votes, and other parliamentary activities.
- The ability to track the progress of bills through the legislative process.
- The ability to subscribe to alerts about specific MPs, bills, or topics.
- A forum for discussing current events in Polish politics.
Sejm 2.0 is still under development, but it is already a valuable resource for anyone who wants to stay informed about what is happening in the Polish parliament.

### Running

celery worker

```bash
celery -A core worker -l INFO --pool=solo
```
