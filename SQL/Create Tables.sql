/* DROP TABLE IF EXISTS `alarme`; 
DROP TABLE IF EXISTS `melder`;

-- Tabelle "melder"
CREATE TABLE melder (
  MelderNr TEXT PRIMARY KEY,
  Gruppe INTEGER NOT NULL,
  Nr_in_Gruppe INTEGER NOT NULL,
  Raum TEXT NOT NULL,
  PlanPath TEXT NOT NULL
);

-- Tabelle "alarme"
CREATE TABLE alarme (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Art TEXT NOT NULL,
  Timestemp DATE NOT NULL,
  MelderNr TEXT,
  FOREIGN KEY (MelderNr) REFERENCES melder (MelderNr)
);

-- Daten einfügen
INSERT INTO melder (MelderNr, Gruppe, Nr_in_Gruppe, Raum, PlanPath) VALUES
('1/1', 1, 1, 'Büro', ''),
('1/2', 1, 2, 'Pausenraum', '');

INSERT INTO alarme (Art, Timestemp, MelderNr) VALUES
('Test5', '0010-00-00', '1/1'); */

/* UPDATE melder SET PlanPath = "./Plaene/Melder1_2.jpg" WHERE MelderNr = '1/2'; */
/* DELETE FROM alarme; */