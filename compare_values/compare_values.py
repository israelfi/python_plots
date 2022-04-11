import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

min_val = 2.825
max_val = 6.296

sim = 'calculated_values.txt'
sim_values = []
with open(sim, 'r') as f:
    a = f.readlines()
    for line in a:
        sim_values.append(float(line.split('0\t')[1].split('\n')[0]))

dhc = 'historical_values.txt'
dhc_values = []
with open(dhc, 'r') as f:
    a = f.readlines()
    for line in a:
        dhc_values.append(float(line.split('0\t')[1].split('\n')[0]))

new_dhc_values = [dhc_values[0]]
for i in range(1, len(dhc_values)):
    aux = (dhc_values[i - 1] + dhc_values[i]) / 2
    new_dhc_values.append(dhc_values[i - 1])
    new_dhc_values.append(aux)

new_dhc_values.append(dhc_values[-1])

diff = []
diff_abs = []
for i in range(len(new_dhc_values)):
    diff.append((new_dhc_values[i] - sim_values[i]) / (max_val - min_val) * 100)
    diff_abs.append(new_dhc_values[i] - sim_values[i])

gs = gridspec.GridSpec(2, 2)
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(sim_values[1:])
ax1.grid(True)
ax1.minorticks_on()
ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax1.set_title('Valores Calculados')
ax1.set_ylabel('Valor')

ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(new_dhc_values[1:])
ax2.grid(True)
ax2.minorticks_on()
ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax2.set_title('Valores Históricos')
ax2.set_ylabel('Valor')

ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(diff[1:])
ax3.grid(True)
ax3.minorticks_on()
ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax3.set_title('Diferença percentual entre os valores')
ax3.set_ylabel('Diferença (%)')

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(diff_abs[1:])
ax4.grid(True)
ax4.minorticks_on()
ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax4.set_title('Diferença absoluta entre os valores')
ax4.set_ylabel('Diferença (m)')

plt.tight_layout()
plt.show()
