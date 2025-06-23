-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema hipperdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema hipperdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hipperdb` DEFAULT CHARACTER SET utf8 ;
USE `hipperdb` ;

-- -----------------------------------------------------
-- Table `hipperdb`.`Therapist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`Therapist` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Therapist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `hipperdb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`User` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(32) NOT NULL,
  `password` VARCHAR(24) NOT NULL,
  `cookies` VARCHAR(256) NULL,
  `is_therapist` INT NOT NULL,
  `fk_therapist_id` INT NULL,
  `dark_mode` INT NOT NULL DEFAULT 0,
  `large_font` INT NOT NULL DEFAULT 0,
  `language` VARCHAR(3) NOT NULL DEFAULT 'NL',
  `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_therapist_id_idx` (`fk_therapist_id` ASC) VISIBLE,
  CONSTRAINT `fk_therapist_id`
    FOREIGN KEY (`fk_therapist_id`)
    REFERENCES `hipperdb`.`Therapist` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `hipperdb`.`Goal`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`Goal` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Goal` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `patient_id_goal` INT NOT NULL,
  `patient_goal` INT NOT NULL,
  `type` ENUM('daily', 'weekly', 'monthly') NOT NULL,
  `reached` TINYINT NOT NULL DEFAULT 0,
  `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `patient_id_goal_idx` (`patient_id_goal` ASC) VISIBLE,
  CONSTRAINT `fk_patient_id_goal`
    FOREIGN KEY (`patient_id_goal`)
    REFERENCES `hipperdb`.`User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `hipperdb`.`Device`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`Device` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Device` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `patient_id_device` INT NULL,
  `device_label` VARCHAR(10) NOT NULL,
  `device_id` INT NOT NULL,
  `auth_token` VARCHAR(32) NOT NULL,
  `last_activity_pull` DATETIME NULL,
  `last_day_data_pull` DATETIME NULL,
  `device_mac_addr` VARCHAR(17) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `patient_id_idx` (`patient_id_device` ASC) VISIBLE,
  UNIQUE INDEX `auth_token_UNIQUE` (`auth_token` ASC) VISIBLE,
  UNIQUE INDEX `device_mac_addr_UNIQUE` (`device_mac_addr` ASC) VISIBLE,
  CONSTRAINT `fk_patient_id_device`
    FOREIGN KEY (`patient_id_device`)
    REFERENCES `hipperdb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `hipperdb`.`Data`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`Data` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `device_id` INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `steps` INT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `PAM_score` FLOAT NOT NULL,
  `zone_1` INT NOT NULL,
  `zone_2` INT NOT NULL,
  `zone_3` INT NOT NULL,
  `patient_id` INT NOT NULL,
  INDEX `device_id_idx` (`device_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_device_id`
    FOREIGN KEY (`device_id`)
    REFERENCES `hipperdb`.`Device` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `hipperdb`.`Patient_has_Therapist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`Patient_has_Therapist` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`Patient_has_Therapist` (
  `patient_id` INT NOT NULL,
  `therapist_id` INT NOT NULL,
  PRIMARY KEY (`patient_id`, `therapist_id`),
  INDEX `fk_phasth_therapist_id_idx` (`therapist_id` ASC) VISIBLE,
  CONSTRAINT `fk_phasth_therapist_id`
    FOREIGN KEY (`therapist_id`)
    REFERENCES `hipperdb`.`Therapist` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_phasth_patient_id`
    FOREIGN KEY (`patient_id`)
    REFERENCES `hipperdb`.`User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `hipperdb`.`MinuteData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hipperdb`.`MinuteData` ;

CREATE TABLE IF NOT EXISTS `hipperdb`.`MinuteData` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `device_id` INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `steps` INT NOT NULL,
  `pam_score` DECIMAL(1) NOT NULL,
  `data_label` VARCHAR(45) NOT NULL,
  `patient_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `device_id_idx` (`device_id` ASC) VISIBLE,
  CONSTRAINT `device_id_fk`
    FOREIGN KEY (`device_id`)
    REFERENCES `hipperdb`.`Device` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `hipperdb`.`Therapist`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`Therapist` (`id`, `name`) VALUES (1, 'hans');
INSERT INTO `hipperdb`.`Therapist` (`id`, `name`) VALUES (2, 'super');

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`User`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`User` (`id`, `name`, `email`, `password`, `cookies`, `is_therapist`, `fk_therapist_id`, `is_superuser`, `dark_mode`, `large_font`, `language`) VALUES (1, 'Henk Man', 'henk.man@gmail.com', 'admin', NULL, 0, NULL, 0, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO `hipperdb`.`User` (`id`, `name`, `email`, `password`, `cookies`, `is_therapist`, `fk_therapist_id`, `is_superuser`, `dark_mode`, `large_font`, `language`) VALUES (2, 'hans', 'hans@gmail.com', 'admin', NULL, 1, 1, 0, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO `hipperdb`.`User` (`id`, `name`, `email`, `password`, `cookies`, `is_therapist`, `fk_therapist_id`,`is_superuser`,  `dark_mode`, `large_font`, `language`) VALUES (3, 'super', 'super@gmail.com', 'super', NULL, 1, 2, 1, DEFAULT, DEFAULT, DEFAULT);


COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`Goal`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`Goal` (`id`, `patient_id_goal`, `patient_goal`, `type`, `reached`) 
VALUES 
  (1, 1, 150, 'daily', 0),
  (2, 1, 600, 'weekly', 0),
  (3, 1, 2000, 'monthly', 0);

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`Device`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`Device` (`id`, `patient_id_device`, `device_label`, `device_id`, `auth_token`, `last_activity_pull`, `last_day_data_pull`, `device_mac_addr`) VALUES (1, 1, '09234', 1, '1234567890', NOW(), NOW(), 'C1:08:00:01:23:B0');

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`Data`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`Data` (`device_id`, `timestamp`, `steps`, `PAM_score`, `zone_1`, `zone_2`, `zone_3`, `patient_id`)
VALUES
  (1, '2025-06-16 12:00:00', 100, 73.4, 30, 40, 30, 1),
  (1, '2025-06-16 12:01:00', 120, 75.0, 35, 45, 40, 1),
  (1, '2025-06-16 12:02:00', 110, 74.0, 32, 38, 40, 1),
  (1, '2025-06-16 12:03:00', 130, 76.0, 33, 47, 50, 1);
  

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`Patient_has_Therapist`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`Patient_has_Therapist` (`patient_id`, `therapist_id`) VALUES (1, 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`MinuteData`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`MinuteData` (`id`, `device_id`, `timestamp`, `steps`, `pam_score`, `data_label`, `patient_id`) 
VALUES 
(1, 1, '2025-06-17 14:30:00', 10, 1.3, 'test', 1),
(2, 1, '2025-06-18 14:30:00', 27, 5, 'test', 1),
(3, 1, '2025-06-18 16:30:00', 47, 4, 'test', 1),
(4, 1, '2025-06-19 18:30:00', 65, 4.8, 'test', 1),
(5, 1, '2025-06-21 14:30:00', 50, 2.9, 'test', 1);


COMMIT;