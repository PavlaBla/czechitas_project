CREATE TABLE "all_in_one" AS
SELECT
    "createdAt", "data_priceTotal", "data_price", "data_priceType", 
    "data_arrangement", "data_livingArea", "data_address", "data_energyClass", 
    "id", "data_city", "data_buildingType", "data_district", "data_offerType", 
    "data_equipment", "data_ownership", "data_propertyState", 
    "data_type", "data_url", "isLive", "markAsDeadAt"
FROM
    "dataset"
WHERE "data_url" NOT LIKE '%idnes%'
    AND "data_type" LIKE 'apartment'
    AND "data_offerType" NOT LIKE 'auction'
    AND "data_address" ILIKE ANY ('%Praha%', '%Brno%', '%Ostrava%', '%Plzeň%', '%Liberec%', '%Olomouc%', '%České Budějovice%', '%Hradec Králové%', '%Pardubice%', '%Ústí nad Labem%', '%Karlovy Vary%', '%Jihlava%', '%Zlín%')
    AND "data_arrangement" IN ('1+0', '1+kk', '1+1', '2+kk', '2+1', '3+kk', '3+1', '4+1', '4+kk')
    AND LOWER("data_address") LIKE '%' || LOWER("data_city") || '%';

// vybrany jen potrebne sloupce a dataset ocisten o radky, ktere nevyhovovaly nasim pozadavkum 
// nebo mely chybne vyplnene adresy
