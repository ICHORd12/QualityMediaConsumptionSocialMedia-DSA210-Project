# QualityMediaConsumptionSocialMedia-DSA210-Project
-----------------------------------------

## **Project Overview**
I am a student from Sabancı University **Ege Büyükacaroğlu** and in this project i will be analysing my types of media consumption In a three week period (31.03.2025-20.04.2025) . This project aims to show the connection between social media consumption and Quality Media Consumption, Alongside with my media consumption habit.

---
## **What is defined as Quality Media?**
 - I define quality media as type of media which to be able to produced and create a narrative requires a cumilative effort for various creative minds alongside with a budget this consist of:
   , Films
   , Comics/Mangas
   , Story Driven Video Games
- Social Media's I primarily use:
  , Youtube
  , Reddit
  , Instagram

---
## **Motivation**
   - I am aiming to figure out relation between my two types of media consumption and in the end want to find the answer my which social media site consumption hinders my quality media consumption the most.
   - I also want to differantiate my media consumption by Work Day/Holiday
---

## **Dataset**
- **Date:** Date of the record (DD/MM/YYYY)
- **Film/TV Series Consumption** Total amount of Film watched through week. (Hours A.B) For A.B notation explanation [^NOTE]
- **Comıc/Manga** Total amount of Comıc/Manga consumption through week. (Hours A.B)
- **Story Driven Video Games** Total amount of Comıc/Manga consumption through week. (Hours A.B)
- **Instagram Usage:** Amount of time i usa Instagram through week. (Hours A.B)
- **Reddit Usage:** Amount of time i usa Reddit through week. (Hours A.B)
- **Youtube Usage:** Amount of time i usa Youtube through week. (Hours A.B)
- **Total Quality Media Consumption:** Total amount of quality media consumption. (Hours A.B)
- **Holiday:** is the day holiday(1) or Work Day(0)? (0-1)
  [^NOTE]: **NOTE:** A.B Where A denotes hours range [0-+inf), B denotes minutes range [0-59]. !Also graph indicators does not follow this format! they follow mins/60 format
### **Methodes of Data Gathering**
 - All Social Media Time will be gathered from shared Screen Time function across Apple Ecosystem (Iphone/Ipad/Macbook)
 - **Film Consumption** will be from gathered IMDB Log's.
 - **Comıc/Manga consumption** will be gathered from apple Screen Time of Chunky App (Only way i use to consume this media type)
 - **Story Driven Video Games** will be gathered from Steam API (Using Playnite)
 - Holiday's will be Saturdays,Sundays,Mondays,Tuesdays and offical Holiday Dates
 ---
 ##**Hypothesis Testing**
 **Default significance : α =0.05** 
 ### **Hypothesis 1**
 - **Null Hypothesis (H₀):** There is no meaningfull connection between my Quality Media Consumption and Social media consumption
 - **Alternative Hypothesis (Hₐ):** There is a meaningfull connection between Quality Media consumption and Social media consumption
 - **Method Used :** Pearson Correlation and Randomization Test
 ---
 #### **Hypothesis 1: Result**
 -**P-Value :** 0.8479
 -**Conclusion** Fail to reject the null hypothesis  there are not enough evidence
 ---
 ### **Hypothesis 2**
 -**Null Hypothesis (H₀):** There is no meaningful connection between my Quality Media Consumption and Day Type (X ₀ = X ₐ)
 -**Alternative Hypothesis (Hₐ):** There is a meaningful connection between Quality Media consumption and Day Type (X ₀ != X ₐ)
 -**Method Used :** Two Sampled T-test
 ---
 #### **Hypothesis 2: Result**
 -**P-Value :** 0.2672
 -**Conclusion** Fail to reject the null hypothesis  there are not enough evidence
 ---
 ### **Hypothesis 3**
 -**Null Hypothesis (H₀):** There is no meaningful connection between my Social Media Consumption and Day Type (X ₀ = X ₐ)
 -**Alternative Hypothesis (Hₐ):** There is a meaningful connection between Social Media consumption and Day Type (X ₀ != X ₐ)
 -**Method Used :** Two Sampled T-test
---
#### **Hypothesis 3: Result**
 -**P-Value :** 0.2982
 -**Conclusion** Fail to reject the null hypothesis  there are not enough evidence
---
 ### **Hypothesis 4**
 -**Null Hypothesis (H₀):** Different platforms does not effect quality media usage differently(U1 = U2 = U3 )
 -**Alternative Hypothesis (Hₐ):** Different platforms does  effect quality media usage differently (Any Differs) 
 -**Method Used :** ANNOVA
---
#### **Hypothesis 4: Result**
 -**P-Value :** 0.9989
 -**Conclusion** Fail to reject the null hypothesis  there are not enough evidence
 


 
 

  
  
