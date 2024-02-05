CREATE TABLE `pokemon_moves` (
  `pok_id` int(11) NOT NULL,
  `version_group_id` int(11) NOT NULL,
  `move_id` int(11) NOT NULL,
  `method_id` int(11) NOT NULL,
  `level` int(11) NOT NULL
);

CREATE TABLE `moves` (
  `move_id` int(11) NOT NULL,
  `move_name` varchar(79) NOT NULL,
  `type_id` int(11) NOT NULL,
  `move_power` smallint(6) DEFAULT NULL,
  `move_pp` smallint(6) DEFAULT NULL,
  `move_accuracy` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`move_id`)
);

CREATE TABLE `pokemon_habitats` (
  `hab_id` int(11) NOT NULL,
  `hab_name` varchar(79) NOT NULL,
  `hab_descript` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`hab_id`)
);

CREATE TABLE `version_groups` (
  `version_id` int(11) NOT NULL,
  `version_name` varchar(79) NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`version_id`)
);

CREATE TABLE `pokemon_move_methods` (
  `method_id` int(11) NOT NULL,
  `method_name` varchar(79) NOT NULL,
  PRIMARY KEY (`method_id`)
);

CREATE TABLE `pokemon_abilities` (
  `pok_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `slot` int(11) NOT NULL,
  PRIMARY KEY (`pok_id`,`slot`)
);

CREATE TABLE `pokemon_evolution` (
  `evol_id` int(11) NOT NULL,
  `evolved_species_id` int(11) NOT NULL,
  `evol_minimum_level` int(11) DEFAULT NULL,
  PRIMARY KEY (`evol_id`)
);

CREATE TABLE `pokemon_evolution_matchup` (
  `pok_id` int(11) NOT NULL,
  `evolves_from_species_id` int(11) DEFAULT NULL,
  `hab_id` int(11) DEFAULT NULL,
  `gender_rate` int(11) NOT NULL,
  `capture_rate` int(11) NOT NULL,
  `base_happiness` int(11) NOT NULL,
  PRIMARY KEY (`pok_id`)
);

CREATE TABLE `pokemon` (
  `pok_id` int(11) NOT NULL,
  `pok_name` varchar(79) NOT NULL,
  `pok_height` int(11) DEFAULT NULL,
  `pok_weight` int(11) DEFAULT NULL,
  `pok_base_experience` int(11) DEFAULT NULL,
  PRIMARY KEY (`pok_id`)
);

CREATE TABLE `type_efficacy` (
  `damage_type_id` int(11) NOT NULL,
  `target_type_id` int(11) NOT NULL,
  `damage_factor` int(11) NOT NULL,
  PRIMARY KEY (`damage_type_id`,`target_type_id`)
);

CREATE TABLE `types` (
  `type_id` int(11) NOT NULL,
  `type_name` varchar(79) NOT NULL,
  `damage_type_id` int(11) DEFAULT NULL
);

CREATE TABLE `pokemon_types` (
  `pok_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `slot` int(11) NOT NULL,
  PRIMARY KEY (`pok_id`,`slot`)
);

CREATE TABLE `trainers` ( 
    `trainer` varchar(120) NOT NULL,
    `pokemon` varchar(79) null,
    `level` int(11) null,
    `hp` int(11) null,
    `attack` int(11) null,
    `defense` int(11) null,
    `spatk` int(11) null,
    `spdef` int(11) null,
    `speed` int(11) null
);

CREATE TABLE `base_stats` (
  `pok_id` int(11) NOT NULL,
  `hp` int(11) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `spatk` int(11) DEFAULT NULL,
  `spdef` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL,
  PRIMARY KEY (`pok_id`)
);

CREATE TABLE `abilities` (
  `id` int(11) NOT NULL,
  `name` varchar(79) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `natures` (
  `name` varchar(12) NOT NULL,
  `increases` varchar(12) NOT NULL,
  `decreases` varchar(12) NOT NULL, 
  PRIMARY KEY (`name`)
);