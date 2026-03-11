-- Schema equivalente ao banco local atual (SQLAlchemy + SQLite)
-- Gerado para analise visual no MySQL Workbench
-- Referencia: estado atual dos models em app/models/

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `downloader_python` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `downloader_python`;

-- -----------------------------------------------------
-- Table `downloader_python`.`editais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`editais` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(64) NOT NULL,
  `titulo` VARCHAR(255) NOT NULL,
  `descricao` TEXT NULL,
  `tipo_documento` VARCHAR(64) NOT NULL,
  `situacao` VARCHAR(100) NULL,
  `synced_at` DATETIME NULL,
  `modalidades_count` INT NOT NULL,
  `vagas_count` INT NOT NULL,
  `anexos_count` INT NOT NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_editais_codigo` (`codigo` ASC),
  INDEX `ix_editais_codigo` (`codigo` ASC)
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`modalidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`modalidades` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `edital_id` INT NOT NULL,
  `codigo` VARCHAR(64) NULL,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` TEXT NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_modalidades_edital_id` (`edital_id` ASC),
  INDEX `ix_modalidades_codigo` (`codigo` ASC),
  CONSTRAINT `fk_modalidades_editais`
    FOREIGN KEY (`edital_id`)
    REFERENCES `downloader_python`.`editais` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`vagas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`vagas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `edital_id` INT NOT NULL,
  `modalidade_id` INT NULL,
  `codigo` VARCHAR(64) NULL,
  `titulo` VARCHAR(255) NOT NULL,
  `descricao` TEXT NULL,
  `quantidade` INT NULL,
  `turno` VARCHAR(100) NULL,
  `local` VARCHAR(255) NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_vagas_edital_id` (`edital_id` ASC),
  INDEX `ix_vagas_modalidade_id` (`modalidade_id` ASC),
  INDEX `ix_vagas_codigo` (`codigo` ASC),
  CONSTRAINT `fk_vagas_editais`
    FOREIGN KEY (`edital_id`)
    REFERENCES `downloader_python`.`editais` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vagas_modalidades`
    FOREIGN KEY (`modalidade_id`)
    REFERENCES `downloader_python`.`modalidades` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`categorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `descricao` TEXT NOT NULL,
  `versao` INT NOT NULL,
  `status` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`inscricoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`inscricoes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `edital_id` INT NULL,
  `vaga_id` INT NULL,
  `status` VARCHAR(50) NOT NULL,
  `inicio` DATETIME NULL,
  `fim` DATETIME NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_inscricoes_edital_id` (`edital_id` ASC),
  INDEX `ix_inscricoes_vaga_id` (`vaga_id` ASC),
  CONSTRAINT `fk_inscricoes_editais`
    FOREIGN KEY (`edital_id`)
    REFERENCES `downloader_python`.`editais` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_inscricoes_vagas`
    FOREIGN KEY (`vaga_id`)
    REFERENCES `downloader_python`.`vagas` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`grupos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`grupos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `categoria_id` INT NULL,
  `nome` VARCHAR(120) NOT NULL,
  `descricao` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_grupos_categoria_id` (`categoria_id` ASC),
  CONSTRAINT `fk_grupos_categorias`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `downloader_python`.`categorias` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`subgrupos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`subgrupos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `grupo_id` INT NULL,
  `nome` VARCHAR(120) NOT NULL,
  `descricao` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_subgrupos_grupo_id` (`grupo_id` ASC),
  CONSTRAINT `fk_subgrupos_grupos`
    FOREIGN KEY (`grupo_id`)
    REFERENCES `downloader_python`.`grupos` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`anexos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`anexos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `edital_id` INT NOT NULL,
  `vaga_id` INT NULL,
  `inscricao_id` INT NULL,
  `categoria_id` INT NULL,
  `subgrupo_id` INT NULL,
  `codigo` VARCHAR(64) NULL,
  `nome` VARCHAR(255) NOT NULL,
  `tipo_documento` VARCHAR(64) NULL,
  `extensao` VARCHAR(20) NULL,
  `url` VARCHAR(500) NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_anexos_edital_id` (`edital_id` ASC),
  INDEX `ix_anexos_vaga_id` (`vaga_id` ASC),
  INDEX `ix_anexos_inscricao_id` (`inscricao_id` ASC),
  INDEX `ix_anexos_categoria_id` (`categoria_id` ASC),
  INDEX `ix_anexos_subgrupo_id` (`subgrupo_id` ASC),
  INDEX `ix_anexos_codigo` (`codigo` ASC),
  CONSTRAINT `fk_anexos_editais`
    FOREIGN KEY (`edital_id`)
    REFERENCES `downloader_python`.`editais` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_anexos_vagas`
    FOREIGN KEY (`vaga_id`)
    REFERENCES `downloader_python`.`vagas` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_anexos_inscricoes`
    FOREIGN KEY (`inscricao_id`)
    REFERENCES `downloader_python`.`inscricoes` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_anexos_categorias`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `downloader_python`.`categorias` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_anexos_subgrupos`
    FOREIGN KEY (`subgrupo_id`)
    REFERENCES `downloader_python`.`subgrupos` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`documentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`documentos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `anexo_id` INT NULL,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` TEXT NULL,
  `url` VARCHAR(500) NULL,
  `raw_payload` JSON NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_documentos_anexo_id` (`anexo_id` ASC),
  CONSTRAINT `fk_documentos_anexos`
    FOREIGN KEY (`anexo_id`)
    REFERENCES `downloader_python`.`anexos` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `downloader_python`.`sync_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `downloader_python`.`sync_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `edital_id` INT NULL,
  `categoria_id` INT NULL,
  `codigo_edital` VARCHAR(64) NOT NULL,
  `tipo_documento` VARCHAR(64) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `message` TEXT NULL,
  `payload_summary` JSON NULL,
  `started_at` DATETIME NOT NULL,
  `finished_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `ix_sync_logs_edital_id` (`edital_id` ASC),
  INDEX `ix_sync_logs_categoria_id` (`categoria_id` ASC),
  INDEX `ix_sync_logs_codigo_edital` (`codigo_edital` ASC),
  CONSTRAINT `fk_sync_logs_editais`
    FOREIGN KEY (`edital_id`)
    REFERENCES `downloader_python`.`editais` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sync_logs_categorias`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `downloader_python`.`categorias` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
