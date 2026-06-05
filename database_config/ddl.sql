-- create database Piscis;
-- USE Piscis;
	create table User (User_ID int(5),
						Username char(50),
						Email varchar(80) not null,
						Password varchar(20) not null,
						ProjectNumber int(20),
						primary key (User_ID)
						);

	create table CPU(CPU_ID INT(5),
					 Name varchar(50) not null,
					 Manufacturer char(30),
					 CPU_Socket varchar(20) not null,
					 CPU_TDP int(20) not null,
					 Have_GPU boolean not null,
					 primary key (CPU_ID)
					);
	create table MotherBoard(MB_ID int(5),
							 Name varchar(50) not null,
							 Manufacturer char(30),
							 MB_Socket varchar(20) not null,
							 Chipset varchar(20) not null,
							 form_factor varchar(30) not null,
							 dimensions_mm varchar(30) not null,
							 Slots_Ram int(5) not null,
							 Ram_type varchar(20) not null,
							 Ram_max_vel int(10) not null,
							 Ram_max_cap int(10) not null,
							 Pcie_Version varchar(20) not null,
							 Pcie_x16_slots varchar(20) not null,
							 m2_slots int(10) not null,
							 M2_pcie_version varchar(20) not null,
							 Sata_ports int(5) not null,
							 primary key(MB_ID)
							 );
	create table MEM_RAM(MEM_RAM_ID int,
						 Name varchar(50) not null,
						 Manufacturer char(30), 
						 RAM_type varchar(20),
						 Velocity int(10),
						 Capacity int(10),
						 Cas_Latency varchar(20),
						 primary key (MEM_RAM_ID)
						 );
	create table GPU(GPU_ID int(5),
						 Name varchar(50) not null,
						 Manufacturer char(30), 
						 Pcie_version varchar(20) not null,
						 Pcie_lanes int(5) not null,
						 Tgp int(10) not null,
						 Power_Connectors varchar(30) not null,
						 Length_mm int(10) not null,
						 Ocupated_slots numeric(4,1) not null,
						 primary key (GPU_ID)
						 );
	create table SSD(SSD_ID int(5),
					 Name varchar(50) not null,
					 Manufacturer char(30), 
					 Interface varchar(20) not null,
					 Format varchar (20) not null,
					 Capacity int(10) not null,
					 primary key(SSD_ID)
					 );
	create table POWER(POWER_ID int(5),
					   Name varchar(50) not null,
					   Manufacturer char(30), 
					   Pot_Watts int(6),
					   Efficiency numeric(4,1) not null,
					   Modular boolean not null,
					   Cpu_8pin_Count int(10) not null,
					   Pcie_8pin_Count int(10) not null,
					   Pcie_12vhpwr_Count int(10) not null,
					   sata_power_count int(5) not null,
					   primary key (POWER_ID)
					   );
	create table Comment(User_ID int(5),
						Component_ID int(5),
						Component_TYPE ENUM('CPU','Placa Mãe','Memória RAM', 'GPU', 'SSD', 'Fonte', 'Site') not null,
						Comment varchar(600) not null,
						foreign key (User_ID) references User(User_ID)
						);
	create table Project(Project_ID int(5),
						 User_ID int(5),
						 Project_name varchar(50),
						 Description varchar(200),
						 MotherBoard_ID int(5),
						CPU_ID int(5),
						GPU_ID int(5),
						MEM_RAM_ID INT(5),
						SSD_ID INT(5),
						POWER_ID INT(5),
						Compatibility boolean not null,
						primary key (Project_ID),
						foreign key (User_ID) references User(User_ID),
						foreign key (MotherBoard_ID) references MotherBoard(MB_ID),
						foreign key (CPU_ID) references CPU(CPU_ID),
						foreign key (GPU_ID) references GPU(GPU_ID),
						foreign key (MEM_RAM_ID) references MEM_RAM(MEM_RAM_ID),
						foreign key (SSD_ID) references SSD(SSD_ID),
						foreign key (POWER_ID) references POWER(POWER_ID)
						);
ALTER TABLE MotherBoard ADD Image_Data MEDIUMBLOB;
ALTER TABLE CPU ADD Image_Data MEDIUMBLOB;
ALTER TABLE GPU ADD Image_Data MEDIUMBLOB;
ALTER TABLE MEM_RAM ADD Image_Data MEDIUMBLOB;
ALTER TABLE SSD ADD Image_Data MEDIUMBLOB;
ALTER TABLE POWER ADD Image_Data MEDIUMBLOB;

ALTER TABLE GPU 
DROP COLUMN Power_Connectors,
ADD Pcie_8pin_Count INT DEFAULT 0,
ADD Pcie_6pin_Count INT DEFAULT 0,
ADD Pcie_12vhpwr_Count INT DEFAULT 0;
ALTER TABLE POWER 
ADD Pcie_6pin_Count INT DEFAULT 0;