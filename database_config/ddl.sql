DROP DATABASE IF EXISTS Piscis;
CREATE DATABASE Piscis;
USE Piscis;

CREATE TABLE User (
    User_ID INT(5) AUTO_INCREMENT,
    Name CHAR(50),
    Email VARCHAR(80) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    ProjectNumber INT(20) DEFAULT 0,
    PRIMARY KEY (User_ID)
);

CREATE TABLE CPU (
    CPU_ID INT(5),
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    CPU_Socket VARCHAR(20) NOT NULL,
    CPU_TDP INT(20) NOT NULL,
    Have_GPU BOOLEAN NOT NULL,
    Image_Data MEDIUMBLOB,
    PRIMARY KEY (CPU_ID)
);

CREATE TABLE MotherBoard (
    MB_ID INT(5) AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    MB_Socket VARCHAR(20) NOT NULL,
    Chipset VARCHAR(20) NOT NULL,
    form_factor VARCHAR(30) NOT NULL,
    dimensions_mm VARCHAR(30) NOT NULL,
    Slots_Ram INT(5) NOT NULL,
    Ram_type VARCHAR(20) NOT NULL,
    Ram_max_vel INT(10) NOT NULL,
    Ram_max_cap INT(10) NOT NULL,
    Pcie_Version VARCHAR(20) NOT NULL,
    Pcie_x16_slots VARCHAR(20) NOT NULL,
    m2_slots INT(10) NOT NULL,
    M2_pcie_version VARCHAR(20) NOT NULL,
    Sata_ports INT(5) NOT NULL,
    Image_Data MEDIUMBLOB,
    PRIMARY KEY (MB_ID)
);

CREATE TABLE MEM_RAM (
    MEM_RAM_ID INT,
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    RAM_type VARCHAR(20),
    Velocity INT(10),
    Capacity INT(10),
    Cas_Latency VARCHAR(20),
    Image_Data MEDIUMBLOB,
    PRIMARY KEY (MEM_RAM_ID)
);

CREATE TABLE GPU (
    GPU_ID INT(5),
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    Pcie_version VARCHAR(20) NOT NULL,
    Pcie_lanes INT(5) NOT NULL,
    Tgp INT(10) NOT NULL,
    Length_mm INT(10) NOT NULL,
    Ocupated_slots NUMERIC(4,1) NOT NULL,
    Pcie_8pin_Count INT DEFAULT 0,
    Pcie_6pin_Count INT DEFAULT 0,
    Pcie_12vhpwr_Count INT DEFAULT 0,
    Image_Data MEDIUMBLOB,
    PRIMARY KEY (GPU_ID)
);

CREATE TABLE SSD (
    SSD_ID INT(5),
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    Interface VARCHAR(20) NOT NULL,
    Format VARCHAR(20) NOT NULL,
    Capacity INT(10) NOT NULL,
    Image_Data MEDIUMBLOB,
    PRIMARY KEY (SSD_ID)
);

CREATE TABLE POWER (
    POWER_ID INT(5) AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Manufacturer CHAR(30),
    Pot_Watts INT(6),
    Efficiency NUMERIC(4,1) NOT NULL,
    Modular BOOLEAN NOT NULL,
    Cpu_8pin_Count INT(10) NOT NULL,
    Pcie_8pin_Count INT(10) NOT NULL,
    Pcie_12vhpwr_Count INT(10) NOT NULL,
    sata_power_count INT(5) NOT NULL,
    Image_Data MEDIUMBLOB,
    Pcie_6pin_Count INT DEFAULT 0,
    PRIMARY KEY (POWER_ID)
);

CREATE TABLE Project (
    ID INT(5) AUTO_INCREMENT,
    User_id INT(5),
    Project_Name VARCHAR(50),
    Description VARCHAR(200),
    MB_ID INT(5),
    CPU_ID INT(5),
    GPU_ID INT(5),
    MEM_RAM_ID INT(5),
    SSD_ID INT(5),
    POWER_ID INT(5),
    Compatibility BOOLEAN NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (User_id) REFERENCES User(User_ID),
    FOREIGN KEY (MB_ID) REFERENCES MotherBoard(MB_ID),
    FOREIGN KEY (CPU_ID) REFERENCES CPU(CPU_ID),
    FOREIGN KEY (GPU_ID) REFERENCES GPU(GPU_ID),
    FOREIGN KEY (MEM_RAM_ID) REFERENCES MEM_RAM(MEM_RAM_ID),
    FOREIGN KEY (SSD_ID) REFERENCES SSD(SSD_ID),
    FOREIGN KEY (POWER_ID) REFERENCES POWER(POWER_ID)
);

CREATE TABLE Comments (
    ID INT AUTO_INCREMENT,
    UserID INT(5),
    ComponentID INT(5),
    ComponentType ENUM('CPU', 'Placa Mãe', 'Memória RAM', 'GPU', 'SSD', 'Fonte', 'Site'),
    Content VARCHAR(600) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (UserID) REFERENCES User(User_ID)
);

CREATE OR REPLACE VIEW Users AS
SELECT
    User_ID AS ID,
    Name,
    Email,
    Password,
    ProjectNumber
FROM User;

CREATE OR REPLACE VIEW `Mother Board` AS
SELECT * FROM MotherBoard;
