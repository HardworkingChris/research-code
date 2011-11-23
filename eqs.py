dV[t]= ((-dV[t-1]/dTm)+((V[t-1]-dV[t-1])/rC)+input)*dt;
V[t]= ((-V[t-1]/Tm)+((dV[t]-V[t-1])/rC))*dt;
