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
-- Table `hipperdb`.`therapist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`therapist` (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `hipperdb`.`patient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`patient` (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(32) NOT NULL,
  `password` VARCHAR(24) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `hipperdb`.`goal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`goal` (
  `id` INT NOT NULL,
  `patient_id_goal` INT NOT NULL,
  `patient_goal` INT NOT NULL,
  `type` ENUM('daily', 'weekly', 'monthly') NOT NULL,
  `reached` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `patient_id_idx` (`patient_id_goal` ASC) VISIBLE,
  CONSTRAINT `patient_id_goal`
    FOREIGN KEY (`patient_id_goal`)
    REFERENCES `hipperdb`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `hipperdb`.`device`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`device` (
  `id` INT NOT NULL,
  `patient_id_device` INT NOT NULL,
  `device_label` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `patient_id_idx` (`patient_id_device` ASC) VISIBLE,
  CONSTRAINT `patient_id_device`
    FOREIGN KEY (`patient_id_device`)
    REFERENCES `hipperdb`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `hipperdb`.`data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`data` (
  `id` INT NOT NULL,
  `device_id` INT NOT NULL,
  `timestamp` DATETIME NULL,
  `steps` INT NULL DEFAULT CURRENT_TIMESTAMP,
  `PAM_score` FLOAT NULL,
  `zone` INT NULL,
  `data_label` VARCHAR(45) NULL,
  INDEX `device_id_idx` (`device_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `device_id`
    FOREIGN KEY (`device_id`)
    REFERENCES `hipperdb`.`device` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `hipperdb`.`patient_has_therapist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hipperdb`.`patient_has_therapist` (
  `patient_id` INT NOT NULL,
  `therapist_id` INT NOT NULL,
  PRIMARY KEY (`patient_id`, `therapist_id`),
  INDEX `fk_patient_has_therapist_therapist1_idx` (`therapist_id` ASC) VISIBLE,
  INDEX `fk_patient_has_therapist_patient1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_patient_has_therapist_patient1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `hipperdb`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_patient_has_therapist_therapist1`
    FOREIGN KEY (`therapist_id`)
    REFERENCES `hipperdb`.`therapist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `hipperdb`.`therapist`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`therapist` (`id`, `name`, `email`, `password`) VALUES (0, 'hans', 'hans@gmail.com', 'admin123');

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`patient`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`patient` (`id`, `name`, `email`, `password`) VALUES (0, 'henk', 'henk@gmail.com', 'admin123');

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`goal`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`goal` (`id`, `patient_id_goal`, `patient_goal`, `type`, `reached`) VALUES (0, 0, 150, 'daily', 0);

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`device`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`device` (`id`, `patient_id_device`, `device_label`) VALUES (0 , 0, 09234);

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`data`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`data` (`id`, `device_id`, `timestamp`, `steps`, `PAM_score`, `zone`, `data_label`) VALUES (0, 0, NULL, NULL, NULL, NULL, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `hipperdb`.`patient_has_therapist`
-- -----------------------------------------------------
START TRANSACTION;
USE `hipperdb`;
INSERT INTO `hipperdb`.`patient_has_therapist` (`patient_id`, `therapist_id`) VALUES (0, 0);

COMMIT;

