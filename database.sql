CREATE TABLE IF NOT EXISTS `pairs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `key` VARCHAR(255) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `upload_time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);

CREATE TABLE IF NOT EXISTS `statistics`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `itemNum` INT NOT NULL,
  `itemSize` FLOAT NOT NULL,
  `requestNum` INT NOT NULL,
  `missRate` FLOAT NOT NULL,
  `hitRate` FLOAT NOT NULL,
  `datetime` DATETIME DEFAULT NULL,
  CONSTRAINT statistics_key PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `configuration`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `capacity` INT NOT NULL,
  `replacePolicy` TINYINT NOT NULL,
  CONSTRAINT configuration_key PRIMARY KEY(`id`)
);