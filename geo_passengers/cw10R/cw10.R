library(rio)
library(tidyverse)  
library(FactoMineR)
library(factoextra)
library(DescTools)
library(ggplot2)

library(readxl)
df <- read_excel("2024_bdl.xlsx") %>% na.omit()

# 1.	Która stacja w każdym z obszarów badań jest najpopularniejsza i najmniej
#popularna według dziennej wymiany pasażerskiej (tzw. „pytanie na rozgrzewkę” :) )?

# obszar = powiat
library(dplyr)

result <- df %>%
  group_by(powiat) %>%
  slice_max(`dzienna wymiana pasażerska\r\n[liczba osób]`, n = 1, with_ties = FALSE) %>%
  ungroup() %>% 
  select('powiat', 'nazwa stacji', `dzienna wymiana pasażerska\r\n[liczba osób]`)

#2. 2.	Czy wymiana pasażerska na stacjach w danych powiatach jest skorelowana 
#ze zmiennymi z Banku Danych Lokalnych GUS? Uzasadnij załączając odpowiednie zestawienia.

# Correlation between column 9 and columns 12–15
cors <- sapply(12:15, function(i) {
  cor(df[[9]], df[[i]], use = "pairwise.complete.obs")
})

cors

names(cors) <- colnames(df)[12:15]
cors

tibble(cors)

# 3.	Czy stacje węzłowe na liniach kolejowych (więcej niż jedna linia kolejowa na stacji) 
# odznaczają się większą wymianą pasażerską niż położone tylko przy jednej linii kolejowej? 
# Dołącz odpowiednie obliczenia.
df['węzeł'] <- grepl(",", df$`linie kolejowe`)

ggplot(data = df, aes(x=`węzeł`, y=`dzienna wymiana pasażerska\r\n[liczba osób]`, colour = `węzeł`)) +
  geom_boxplot()

df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  group_by(`węzeł`) %>%
  summarise(across(everything(), mean, na.rm = TRUE))

df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  summarise(mean = mean(`dzienna wymiana pasażerska\r\n[liczba osób]`), 
            std=sd(`dzienna wymiana pasażerska\r\n[liczba osób]`), n=n(),
            .by=`węzeł`)

df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  filter(`dzienna wymiana pasażerska\r\n[liczba osób]` < 20000) %>%
  summarise(mean = mean(`dzienna wymiana pasażerska\r\n[liczba osób]`), 
            std=sd(`dzienna wymiana pasażerska\r\n[liczba osób]`), n=n(),
            .by=`węzeł`)

df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  summarise(mean = mean(`dzienna wymiana pasażerska\r\n[liczba osób]`), n = n(), .by=`węzeł`)



df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  filter(`dzienna wymiana pasażerska\r\n[liczba osób]` < 20000) %>%
  group_by(`węzeł`) %>%
  summarise(across(everything(), mean, na.rm = TRUE))



df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`, `nazwa stacji`) %>%
  filter(`dzienna wymiana pasażerska\r\n[liczba osób]` > 20000) 

df %>%
  select(`dzienna wymiana pasażerska\r\n[liczba osób]`, `węzeł`) %>%
  filter(`dzienna wymiana pasażerska\r\n[liczba osób]` < 20000) %>%
  ggplot(aes(fill  = `węzeł`,
             x = `dzienna wymiana pasażerska\r\n[liczba osób]`)) +
  geom_histogram()

library(janitor)
df <- clean_names(df)

#find Q1, Q3, and interquartile range for values in column A
Q1 <- quantile(df$dzienna_wymiana_pasazerska_liczba_osob, .25)
Q3 <- quantile(df$dzienna_wymiana_pasazerska_liczba_osob, .75)
IQR <- IQR(df$dzienna_wymiana_pasazerska_liczba_osob)

#only keep rows in dataframe that have values within 1.5*IQR of Q1 and Q3


cuts <- df %>% select( dzienna_wymiana_pasazerska_liczba_osob, wezel) %>%
  summarise(Q3 = quantile(dzienna_wymiana_pasazerska_liczba_osob, .75), 
            IQR = IQR(dzienna_wymiana_pasazerska_liczba_osob), .by = wezel)

no_outliers <- df  %>% select( dzienna_wymiana_pasazerska_liczba_osob, wezel) %>%
  filter((dzienna_wymiana_pasazerska_liczba_osob < 1800 + 1.5*1650 & wezel==TRUE) | 
           (dzienna_wymiana_pasazerska_liczba_osob < 175 + 1.5*160 & wezel==FALSE))

ggplot(data=no_outliers, aes(x=wezel, y=dzienna_wymiana_pasazerska_liczba_osob, colour = wezel)) +
  geom_boxplot() + labs(x="węzeł", y="dzienna wymiana pasażerska [liczba osób]")
no_outliers %>% summarise(mean = mean(dzienna_wymiana_pasazerska_liczba_osob), 
                          std=sd(dzienna_wymiana_pasazerska_liczba_osob), n=n(),
                          .by=wezel)


# trend dzienna_wymiana y i średnia dobowa ilość zatrzymań
no_outliers <- df  %>% select( dzienna_wymiana_pasazerska_liczba_osob, wezel, srednia_dobowa_liczba_zatrzyman) %>%
  filter((dzienna_wymiana_pasazerska_liczba_osob < 1800 + 1.5*1650 & wezel==TRUE) | 
           (dzienna_wymiana_pasazerska_liczba_osob < 175 + 1.5*160 & wezel==FALSE))

no_outliers %>% 
  filter(wezel==FALSE) %>%
  ggplot(aes(x=srednia_dobowa_liczba_zatrzyman, y=dzienna_wymiana_pasazerska_liczba_osob)) + geom_point() +
  geom_smooth(method = "lm") + ggtitle("Nie węzły")

no_outliers %>% 
  filter(wezel==TRUE) %>%
  ggplot(aes(x=srednia_dobowa_liczba_zatrzyman, y=dzienna_wymiana_pasazerska_liczba_osob)) + geom_point() +
  geom_smooth(method = "lm") + ggtitle("Węzły") + theme_minimal()


library(lmtest)
model <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ srednia_dobowa_liczba_zatrzyman , data=wezel_data)
summary(model)

nie_wezel_data <- no_outliers %>% filter(wezel==FALSE)
model2 <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ srednia_dobowa_liczba_zatrzyman , data=nie_wezel_data)
summary(model2)

model3 <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ I(srednia_dobowa_liczba_zatrzyman^2) , data=wezel_data)

model4 <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ I(srednia_dobowa_liczba_zatrzyman^2) , data=nie_wezel_data)

model_all <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ I(srednia_dobowa_liczba_zatrzyman) , data=df)
model_all2 <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ I(srednia_dobowa_liczba_zatrzyman^2) + log(srednia_dobowa_liczba_zatrzyman), data=df)
model_all_kwadrat <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ I(srednia_dobowa_liczba_zatrzyman^2), data=df)

df %>% ggplot(aes(x=srednia_dobowa_liczba_zatrzyman, y=sqrt(dzienna_wymiana_pasazerska_liczba_osob))) + geom_point() + geom_smooth()

df5 <- df %>% select(powiat, dzienna_wymiana_pasazerska_liczba_osob, ludnosc_w_1000_osob_2024) %>%
  mutate(pasazer_per_1000_osob = dzienna_wymiana_pasazerska_liczba_osob/ludnosc_w_1000_osob_2024) %>%
  summarise(kolej_index = sum(pasazer_per_1000_osob), .by = powiat) 

df5 %>% arrange(kolej_index, descending=FALSE)


og <- df[,1:11] %>% filter(obszar_badan == "Gdańsk") %>% select(-obszar_badan)

og_PODM_J_R <- read_csv("C:/Users/laura/Studia/Geo/Cw10/og_PODM_J_R.csv")
og_PODM_J_R <- clean_names(og_PODM_J_R[,1:3])
og_PODM_J_R <- og_PODM_J_R %>% rename(podmioty_gosp = podmioty_gospodarcze_w_uslugach_wyzszego_rzedu_sekcje_j_r_na_1000_ludnosci_2024)
og_FIN <-read_csv("C:/Users/laura/Studia/Geo/Cw10/og_FIN.csv")
og_FIN  <- clean_names(og_FIN[,1:3])
og_FIN <- og_FIN %>% rename(dochody = gminy_lacznie_z_miastami_na_prawach_powiatu_dochody_wlasne_2024_zl)

og_SZKO <-read_csv("C:/Users/laura/Studia/Geo/Cw10/og_SZKO.csv")
og_SZKO  <- clean_names(og_SZKO[,1:3])

# 1.	Skonstruuj najlepiej dopasowany trend do wykresu rozrzutu zmiennych 
# „dzienna wymiana pasażerska” (OY) i „średnia dobowa liczba zatrzymań” (OX) dla wybranego obszaru badań. 
# Zamieść równanie i wartość współczynnika korelacji. Uzasadnij swój wybór.

og %>% select(dzienna_wymiana_pasazerska_liczba_osob, srednia_dobowa_liczba_zatrzyman) %>%
  ggplot(aes(y = dzienna_wymiana_pasazerska_liczba_osob, x = srednia_dobowa_liczba_zatrzyman)) + geom_smooth() + geom_point()
og_model <- lm(dzienna_wymiana_pasazerska_liczba_osob ~ srednia_dobowa_liczba_zatrzyman, data = og)

# 2.	Porównaj sytuację społeczno-ekonomiczną gmin (na podstawie danych z Banku Danych Lokalnych GUS) posiadających na swoim terenie przynajmniej jedną stację kolejową oraz ich pozbawionych. 
# Czy można powiedzieć, że obecność kolei przekłada się pozytywnie na rozwój społeczno-gospodarczy gmin?
og_GUS <- og_PODM_J_R %>% left_join(og_FIN) %>% left_join(og_SZKO) %>% rename(gmina=nazwa)
og_STACJE <- og %>% summarise(stacje = n(), .by=gmina)

og_GUS <- og_GUS %>% select(-kod) %>% left_join(og_STACJE) %>% replace(is.na(.), 0)
og_GUS <- og_GUS %>% mutate(jest_stacja = stacje > 0)

og_GUS %>% ggplot(aes(y=dochody, colour = jest_stacja, x = jest_stacja)) + geom_boxplot() + 
  ggtitle("Obecność stacji w gminie a dochody na mieszkańca") +
  labs(x="Czy jest stacja?", y="Dochody własne gmin na 1 mieszkańca")


og_GUS %>% ggplot(aes(y=podmioty_gosp, colour = jest_stacja, x = jest_stacja)) + geom_boxplot() + 
  ggtitle("Obecność stacji w gminie a liczba podmiotów gospodarczych wyższego rzędu") +
  labs(x="Czy jest stacja?", y="•	Podmioty gospodarcze w usługach wyższego rzędu (sekcje J-R) na 1000 ludności")

cors <- sapply(2:4, function(i) {
  cor(og_GUS[[5]], og_GUS[[i]], use = "pairwise.complete.obs")
})

cors

names(cors) <- colnames(og_GUS)[2:4]
cors


og_GUS %>% summarise(mean_podmioty = mean(podmioty_gosp), mean_dochody = mean(dochody), mean_szk = mean(szkoly), .by=jest_stacja)
