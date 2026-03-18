library(bibliometrix)
library(ggplot2)

# 1. Lendo sua base unificada (que já contém Scopus e WoS)
# Usamos 'scopus' aqui apenas como um "tradutor" de etiquetas, 
# ele vai processar todos os 700+ artigos que estão no seu arquivo.
M <- convert2df("Database1.csv", dbsource = "scopus", format = "csv")

# 3. Preparar os dados (Contagem de artigos por ano de publicação 'PY')
# Aqui garantimos que o objeto 'dados_anuais' seja criado corretamente
dados_anuais <- as.data.frame(table(M$PY))
colnames(dados_anuais) <- c("Ano", "Artigos")
dados_anuais$Ano <- as.numeric(as.character(dados_anuais$Ano))

# 4. Criar o gráfico com os padrões da revista
# No Linux, 'sans' é o equivalente ao Arial. 174mm = 6.85 polegadas
grafico_final <- ggplot(dados_anuais, aes(x = Ano, y = Artigos)) +
  geom_line(color = "#192338", size = 0.5) + 
  geom_point(size = 1.2) +
  theme_bw() + 
  theme(
    panel.grid.minor = element_blank(),
    plot.title = element_blank(),
    # Fonte 8pt (Arial/Sans)
    text = element_text(family = "sans", size = 8),
    axis.title = element_text(size = 8),
    axis.text = element_text(size = 8)
  ) +
  labs(x = "Year", y = "Number of Scientific Articles")

# 5. Salvar em TIFF (600 DPI, 174mm de largura)
tiff("Figura_Producao_Anual_600DPI.tiff", 
     width = 174, 
     height = 90, # Altura proporcional
     units = "mm", 
     res = 600, 
     compression = "lzw")

print(grafico_final)

dev.off() # Fecha e salva o arquivo


##--------------------------------------##

library(bibliometrix)
library(ggplot2)
library(dplyr)
library(tidyr)
library(stringr)
library(maps)
library(patchwork) 

# ==============================================================================
# 1. CARREGAR E LIMPAR OS DADOS
# ==============================================================================
M <- convert2df("Database1.csv", dbsource = "scopus", format = "csv")
M <- metaTagExtraction(M, Field = "AU_CO", sep = ";")

links_limpos <- M %>%
  select(AU_CO) %>%
  filter(!is.na(AU_CO) & AU_CO != "") %>%
  mutate(id = row_number()) %>%
  separate_rows(AU_CO, sep = ";") %>%
  mutate(AU_CO = str_trim(str_to_upper(AU_CO))) %>%
  mutate(region = case_when(
    str_detect(AU_CO, "USA|UNITED STATES") ~ "USA",
    str_detect(AU_CO, "CHINA|PEOPLES R CHINA") ~ "China",
    str_detect(AU_CO, "UNITED KINGDOM|ENGLAND|SCOTLAND|WALES|UK") ~ "UK",
    str_detect(AU_CO, "SOUTH AFRICA") ~ "South Africa",
    str_detect(AU_CO, "BRAZIL") ~ "Brazil",
    str_detect(AU_CO, "CHILE") ~ "Chile",
    str_detect(AU_CO, "ARGENTINA") ~ "Argentina",
    str_detect(AU_CO, "RUSSIAN FEDERATION|RUSSIA") ~ "Russia",
    str_detect(AU_CO, "GERMANY") ~ "Germany",
    str_detect(AU_CO, "SOUTH KOREA|KOREA") ~ "South Korea",
    str_detect(AU_CO, "NEW ZEALAND") ~ "New Zealand",
    TRUE ~ str_to_title(word(AU_CO, -1))
  ))

# ==============================================================================
# 2. CRIAR O MAPA a: PRODUÇÃO CIENTÍFICA
# ==============================================================================
df_paises <- links_limpos %>%
  group_by(region) %>%
  summarise(Artigos = n())

world_map <- map_data("world")
map_data_final <- left_join(world_map, df_paises, by = "region")

mapa_final <- ggplot(map_data_final, aes(x = long, y = lat, group = group)) +
  geom_polygon(fill = "#f8f9fa", color = "#d1d1d1", linewidth = 0.05) +
  geom_polygon(aes(fill = Artigos), color = "white", linewidth = 0.05) +
  scale_fill_gradientn(
    colors = c("#d9f5f0", "#75e2e0", "#2cacad", "#024d60", "#192338"),
    trans = "log10",
    breaks = c(1, 10, 50, 100, 500),
    labels = c("1", "10", "50", "100", "500+"),
    na.value = "#d1d1d1"
  ) +
  coord_fixed(1.3) +
  theme_void() +
  theme(
    text = element_text(family = "sans", size = 8),
    legend.position = "bottom",
    legend.key.width = unit(10, "mm"),
    legend.title = element_text(size = 8, face = "bold", vjust = 1),
    legend.text = element_text(size = 8),
    plot.margin = margin(2, 2, 2, 2, "mm")
  ) +
  labs(fill = "Production")

# ==============================================================================
# 3. CRIAR O MAPA b: REDE DE COLABORAÇÃO
# ==============================================================================
par_colab <- links_limpos %>%
  inner_join(links_limpos, by = "id", relationship = "many-to-many") %>%
  filter(region.x < region.y) %>% 
  group_by(region.x, region.y) %>%
  summarise(Peso = n(), .groups = 'drop')

par_colab_filtrado <- par_colab %>% filter(Peso >= 1)

tamanho_nos <- par_colab_filtrado %>%
  pivot_longer(cols = c(region.x, region.y), names_to = "tipo", values_to = "region") %>%
  group_by(region) %>%
  summarise(Total_Colab = sum(Peso))

capitais <- maps::world.cities %>%
  filter(capital == 1) %>%
  select(region = country.etc, lat_cap = lat, long_cap = long) %>%
  distinct(region, .keep_all = TRUE)

world_coords <- map_data("world") %>%
  group_by(region) %>%
  summarise(long_med = mean(range(long)), lat_med = mean(range(lat)))

coords_finais <- world_coords %>%
  left_join(capitais, by = "region") %>%
  mutate(lat = ifelse(!is.na(lat_cap), lat_cap, lat_med),
         long = ifelse(!is.na(long_cap), long_cap, long_med)) %>%
  select(region, lat, long)

coords_plot <- coords_finais %>%
  inner_join(tamanho_nos, by = "region")

colab_map_data <- par_colab_filtrado %>%
  left_join(coords_finais, by = c("region.x" = "region")) %>%
  left_join(coords_finais, by = c("region.y" = "region")) %>%
  filter(!is.na(long.x) & !is.na(long.y))

mapa_rede_final <- ggplot() +
  geom_polygon(data = map_data("world"), aes(x = long, y = lat, group = group), 
               fill = "#d1d1d1", color = "white", linewidth = 0.1) +
  geom_curve(data = colab_map_data, 
             aes(x = long.x, y = lat.x, xend = long.y, yend = lat.y, 
                 linewidth = Peso, alpha = Peso),
             color = "#2cacad", curvature = 0.2) +
  geom_point(data = coords_plot, 
             aes(x = long, y = lat, size = Total_Colab), 
             color = "#192338", alpha = 0.9) +
  scale_linewidth_continuous(range = c(0.1, 3.5)) +
  scale_alpha_continuous(range = c(0.15, 0.85), guide = "none") + 
  scale_size_continuous(range = c(0.5, 4.0), guide = "none") +    
  coord_fixed(1.3) +
  theme_void() +
  theme(
    text = element_text(family = "sans", size = 8),
    legend.position = "bottom",
    legend.key.width = unit(10, "mm"),
    legend.title = element_text(size = 8, face = "bold", vjust = 1),
    legend.text = element_text(size = 8),
    plot.margin = margin(2, 6, 2, 2, "mm")
  ) +
  labs(linewidth = "Co-authorship")

# ==============================================================================
# 4. UNIR E SALVAR O PAINEL FINAL
# ==============================================================================
painel_completo <- mapa_final + mapa_rede_final + 
  plot_annotation(tag_levels = 'a') &  # Letras a e b em minúsculo
  theme(plot.tag = element_text(size = 8, face = "bold", family = "sans")) # Fonte rigorosamente em 8pt

# Salvar com 174mm de largura total
tiff("Figura2_Painel_Producao_e_Rede_174mm.tiff", 
     width = 174, height = 90, units = "mm", res = 600, compression = "lzw")
print(painel_completo)
dev.off()

# ==============================================================================

