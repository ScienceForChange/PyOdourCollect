# PyOdourCollect
> Python3 bindings and command line tool to access OdourCollect's Citizen Observatory data in real time.

This python module provides a basic, read only interface with [OdourCollect.eu](https://odourcollect.eu)'s odour observation data API, as well as a command line tool to download data from OdourCollect directly info a CSV or a XLSX file.
It also provides some data enrichment features not available in OdourCollect.eu webapp that are very useful for data analysis purposes.

Please, check out [USAGE.md](https://github.com/ScienceForChange/PyOdourCollect/blob/main/USAGE.md) to use the module and the CLI tool.
 
## About OdourCollect.eu
[OdourCollect.eu](https://odourcollect.eu) is one of the most acknowledged Citizen Observatories (CO's) in Citizen Science (CS) landscape.
OdourCollect's main goal is providing an open, free platform for the citizens to report odour observations, making a worldwide collaborative odour map.

Albeit it allows reporting nice odours as well as bad ones, it has become popular for its potential to provide hard evidence of bad odour episodes 
happening in neighborhoods that are affected by odour emiting facilities like waste water processing, livestock, oil etc.

OdourCollect was an idea of Rosa Arias, CEO and founder of [Science for Change](https://scienceforchange.eu),  inspired by a standardized European methodology to evaluate odour episodes through field observation, `CEN 16841` which in turn is based on the German standards `VDI3882-1` and `VDI3882-2`. 
The last public version of OdourCollect's open source code can be obtained in [this repository](https://github.com/ScienceForChange/odourcollect.eu).    

OdourCollect has validated its bottom-up methodology in 10 pilot projects in 10 countries (Spain, Portugal, Greece, Bulgaria, Chile, Italy, UK, Germany, Austria and Uganda) and has been supported by Spanish and European grants since it was first launched in 2019:
  - The Research and Innovation program of the European Union Horizon 2020 under agreement No. 789315, in the context of the D-NOSES project.
  - FECYT, the Spanish Foundation for Science and Technology - Ministry of Science and Innovation. 
## About odour pollution
- Frequent exposure to annoying odours can cause headache, stress, anxiety, lack of concentration, insomnia or even increase respiratory problems. 
- Even though ambient odours are the second cause of environmental complaints after noise worldwide, lots of countries worldwide lack a legal regulatory framework to protect citizens' rights and health.
You can learn more about existing regulations in odour pollution in the [D-NOSES Policy brief](https://dnoses.eu/policy-brief).
- If your community is affected by odour pollution problems, you can [contact Science for Change](mailto://hello@scienceforchange.eu) for an evaluation of your case.

## About MECODA and COS4CLOUD
This data parsing library has been specifically developed for [MECODA](https://github.com/eosc-cos4cloud/mecoda-orange), 
a toolkit built around [Orange Data Mining](https://orangedatamining.com/) for Citizen Observatory data analysis.

MECODA is part of the technological services for Citizen Observatories that are developed in the context of 
[COS4CLOUD](https://cos4cloud-eosc.eu/) project, funded by the European Union’s Horizon 2020 research and innovation 
programme under grant agreement #863463.

Please visit [COS4CLOUD's web site](https://cos4cloud-eosc.eu) for more info on how COS4CLOUD empowers Citizen Science with technology and tools.

<img src="https://ec.europa.eu/info/sites/default/themes/europa/images/svg/logo/logo--en.svg" width="240px"/>
<img src="https://cos4cloud-eosc.eu/wp-content/uploads/2020/07/logo-cos4cloud-middle.png" width="240px"/>


## About Science for Change
<img src="https://www.scienceforchange.eu/wp-content/uploads/2021/06/Logos-SfC-color-2.png" width="240px"/>

If you want to tackle a social, environmental or health challenges that require data to be gathered and analysed, you can count on 
Science for Change for designing, developing, creating a community around, or leverage data from a Citizen Observatory.
[Contact Science for Change](mailto://hello@scienceforchange.eu) for an evaluation of your case.
