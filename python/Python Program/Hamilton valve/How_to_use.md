This file explains how to use the class **Valve**. Valve used: Hamilton MVP serial

1. Give the configurations of each of your devices in the file Config.py
	- Number of valve used → NbofValve
	- Port where the first valve is pluged → PortValve
	- Configuration of the valves (number of positions available on the valve, e.g 8). If there are more than one valve, indicate the configuration of each valve in the same order than the adress (a, b, c ...)→ ValveConfigPosition[]
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=Valve()
	
4. Open the connection with the valve :
	VariableName.OpenConnection()
	
5. Select the position you want for target valve :
	VariableName.ValveRotation("b",5)