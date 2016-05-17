SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `FeiFlight` ;
CREATE SCHEMA IF NOT EXISTS `FeiFlight` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `FeiFlight` ;

-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL,
  `user_type` INT NULL,
  `password` VARCHAR(20) NULL,
  `name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `mobile` CHAR(11) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `admin` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `admin` (
  `user_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_admin_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_admin_users_idx` ON `admin` (`user_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `company` (
  `user_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_company_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_company_users1_idx` ON `company` (`user_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `customer` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `customer` (
  `user_id` INT NOT NULL,
  `balance` INT NULL,
  `point` INT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_customer_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_customer_users1_idx` ON `customer` (`user_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `flight`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flight` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `flight` (
  `id` VARCHAR(10) NOT NULL,
  `date` DATE NOT NULL,
  `class` VARCHAR(45) NOT NULL,
  `from` VARCHAR(45) NULL,
  `to` VARCHAR(45) NULL,
  `depart` TIME NULL,
  `arrival` TIME NULL,
  `price` INT NULL,
  `point` INT NULL,
  `cancel_rule` INT NULL,
  `change_rule` INT NULL,
  `volume` INT NULL,
  `canceled` TINYINT(1) NULL,
  `company_id` INT NOT NULL,
  PRIMARY KEY (`id`, `date`, `class`),
  CONSTRAINT `fk_flight_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `company` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_flight_company1_idx` ON `flight` (`company_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `order` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `order` (
  `id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `mobile` VARCHAR(45) NULL,
  `time` DATETIME NULL,
  `price` INT NULL,
  `point` INT NULL,
  `paid` TINYINT(1) NULL,
  `canceled` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_order_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customer` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_order_customer1_idx` ON `order` (`customer_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `passenger`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `passenger` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `passenger` (
  `id` CHAR(11) NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `order_passenger`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `order_passenger` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `order_passenger` (
  `order_id` INT NOT NULL,
  `passenger_id` CHAR(11) NOT NULL,
  PRIMARY KEY (`order_id`, `passenger_id`),
  CONSTRAINT `fk_passenger_has_order_passenger1`
    FOREIGN KEY (`passenger_id`)
    REFERENCES `passenger` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_passenger_has_order_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_passenger_has_order_order1_idx` ON `order_passenger` (`order_id` ASC);

SHOW WARNINGS;
CREATE INDEX `fk_passenger_has_order_passenger1_idx` ON `order_passenger` (`passenger_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `flight_cancel_application`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flight_cancel_application` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `flight_cancel_application` (
  `id` INT NOT NULL,
  `flight_id` VARCHAR(10) NOT NULL,
  `flight_date` DATE NOT NULL,
  `flight_class` VARCHAR(45) NOT NULL,
  `process` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_flight_cancel_application_flight1`
    FOREIGN KEY (`flight_id` , `flight_date` , `flight_class`)
    REFERENCES `flight` (`id` , `date` , `class`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_flight_cancel_application_flight1_idx` ON `flight_cancel_application` (`flight_id` ASC, `flight_date` ASC, `flight_class` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `order_cancel_application`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `order_cancel_application` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `order_cancel_application` (
  `id` INT NOT NULL,
  `order_id` INT NOT NULL,
  `process` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_order_cancel_application_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_order_cancel_application_order1_idx` ON `order_cancel_application` (`order_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `order_flight`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `order_flight` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `order_flight` (
  `order_id` INT NOT NULL,
  `flight_id` VARCHAR(10) NOT NULL,
  `flight_date` DATE NOT NULL,
  `flight_class` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`order_id`, `flight_id`, `flight_date`, `flight_class`),
  CONSTRAINT `fk_order_has_flight_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_has_flight_flight1`
    FOREIGN KEY (`flight_id` , `flight_date` , `flight_class`)
    REFERENCES `flight` (`id` , `date` , `class`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_order_has_flight_flight1_idx` ON `order_flight` (`flight_id` ASC, `flight_date` ASC, `flight_class` ASC);

SHOW WARNINGS;
CREATE INDEX `fk_order_has_flight_order1_idx` ON `order_flight` (`order_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `order_change_application`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `order_change_application` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `order_change_application` (
  `id` INT NULL,
  `order_id` INT NOT NULL,
  `flight_id` VARCHAR(10) NOT NULL,
  `flight_date` DATE NOT NULL,
  `flight_class` VARCHAR(45) NOT NULL,
  `process` VARCHAR(45) NULL,
  PRIMARY KEY (`order_id`, `flight_id`, `flight_date`, `flight_class`),
  CONSTRAINT `fk_order_has_flight_order2`
    FOREIGN KEY (`order_id`)
    REFERENCES `order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_has_flight_flight2`
    FOREIGN KEY (`flight_id` , `flight_date` , `flight_class`)
    REFERENCES `flight` (`id` , `date` , `class`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_order_has_flight_flight2_idx` ON `order_change_application` (`flight_id` ASC, `flight_date` ASC, `flight_class` ASC);

SHOW WARNINGS;
CREATE INDEX `fk_order_has_flight_order2_idx` ON `order_change_application` (`order_id` ASC);

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
