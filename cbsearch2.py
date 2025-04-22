import random
import math

#mengkonversi string biner 5-bit ke integer
def binary_to_int(str_x):
    num = 0
    j = 4
    for i in range(0, 5):
        num += 2**i * int(str_x[j])
        j -= 1
    return num

#memecah kromosom menjadi 2 biner dengan 5 bit kemudian mengembalikan hasil konversinya sesuai metode offset
def decode_chromosome(str_chrom):
    x1 = str_chrom[0:5]
    x2 = str_chrom[5:10]
    return binary_to_int(x1) - 10, binary_to_int(x2) - 10 #offset -10 untuk mempermudah represanti bilangan negatif biner

#fungsi matematika pada soal
def func(x1, x2):
    pers1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
    pers2 = math.exp(1 - math.sqrt(x1**2)) * 3/4
    return (pers1 + pers2) * -1

#mengecek apakah kromosom valid (dalam domain) atau tidak
def num_check(str_chrom):
    x1, x2 = decode_chromosome(str_chrom)
    if x1 >= -10 and x1 <= 10 and x2 >= -10 and x2 <= 10 :
        return True
    else :
        return False

def fitness_calc(str_chrom):
    if num_check(str_chrom) :
        x1, x2 = decode_chromosome(str_chrom)
        return func(x1, x2) * -1 #karena mencari yang menghasilkan nilai minimum dari fungsi, maka dikali dengan -1 agar hasil yang paling kecil bisa memiliki fitness yang paling besar
    else :
        return -10000 #jika angka tidak valid, akan mengembalikan angka fitness yang sangat kecil

#melakukan crossover antara str_par1 dan str_par2 di satu titik acak
def crossover(str_par1, str_par2):
    point = random.randint(1, 9)
    str_chld1 = str_par1[:point] + str_par2[point:]
    str_chld2 = str_par2[:point] + str_par1[point:]
    return str_chld1, str_chld2 

#mengimplementasikan crossover dengan Probabilitas crossover sebesar 80% (0.80)
def crossover_prob(str_par1, str_par2):
    Pc = 0.80

    if random.random() < Pc: 
        child1, child2 = crossover(str_par1,str_par2) #jika angka random yang digenerate <0.80, akan dilakukan crossover
    else:
        child1, child2 = str_par1, str_par2 #jika tidak, child akan langsung mewarisi kromosom masing-masing parent
    return child1, child2

#mengimplementasikan mutasi dengan Probabilitas mutasi sesesar 30%, (0.30)
def mutation_prob(str_chrom):
    bit = "" #variable untuk menampung hasil dari proses mutasi
    Pm = 0.30
    for i in range(0,10): #melakukan perulangan sebanyak bit pada kromosom
        if random.random() < Pm: #jika angka random yang digenerate <0.30, akan dilakukan mutasi
            if str_chrom[i] == "1":
                bit += "0"
            else:
                bit += "1"
        else:
            bit += str_chrom[i] #jika tidak, tidak akan dilakukan mutasi
    return bit

#Seleksi Roulette Wheel
def roulette_wheel_selection(population):
    from random import uniform 

    total_fitness = 0
    fitness_scores = []

    #menghitung total fitness populasi
    for i in range(len(population)):  #(len(population)) untuk jumlah populasi
        fitness = fitness_calc(population[i])
        fitness_scores.append(fitness)
        total_fitness += fitness

    if total_fitness == 0:#jika semua fitness 0 (tidak valid atau sama), semua kromosom diberi peluang yang sama untuk dipilih.
        prob_selection = [1 / len(population)] * len(population) #menghindari pembagian dengan nol jika total fitness = 0
    else:
        prob_selection = [f / total_fitness for f in fitness_scores] #probabilitas seleksi proporsional terhadap fitness(f)

    def select_one(): #memilih 1 chromosom untuk parent
        r = uniform(0, 1) #untuk generate random 0 atau 1
        cumulative_prob = 0.0
        for chrom, prob in zip(population, prob_selection): #menggabungkan list/array population untuk perulangan sehinnga dapat pasangan (chrom, prob).
            cumulative_prob += prob
            if r <= cumulative_prob:
                return chrom

    return select_one(), select_one() #return hasil seleksi 2 parent

def child_procces(parent1, parent2):
    attempts = 0
    while attempts < 10:
        c1, c2 = crossover_prob(parent1, parent2)
        c1 = mutation_prob(c1)
        c2 = mutation_prob(c2)
        if num_check(c1) and num_check(c2):
            return c1, c2
        attempts += 1
    return c1, c2

#menyortir populasi berdasarkan fitness terbesar menggunakan metode selection sort
def sort_population(population):
    pop = population
    for i in range(0,6):
        max = i
        for j in range(i+1,6):
            if fitness_calc(pop[max]) < fitness_calc(pop[j]):
                max = j
        temp = pop[i]
        pop[i] = pop[max]
        pop[max] = temp
    return pop

#menggunakan metode elitsm dan juga generational replacement
def survivor_selection(population):
    #elitsm dengan mempertahankan 2 kromosom terbaik
    pop = sort_population(population)
    best1 = pop[0] 
    best2 = pop[1]
    
    #generational replacement
    par1, par2 = roulette_wheel_selection(population)
    chld1, chld2 = child_procces(par1,par2)

    par3, par4 = roulette_wheel_selection(population)
    chld3, chld4 = child_procces(par3,par4)
    pop = [best1,best2,chld1,chld2,chld3,chld4] #mengumpulkan hasil generasi baru menjadi 1 populasi
    return pop

def genetic_algorithm(generations, initial_pop):
    population = initial_pop
    for gen in range(generations):#perulangan setiap generasi
        print(f"\nGenerasi ke-{gen+1}:")
        sort_population(population) 
        for i in range(len(population)):
            x1, x2 = decode_chromosome(population[i])
            print(f"Kromosom: {population[i]}, x1: {x1}, x2: {x2}, Fitness: {fitness_calc(population[i])}")
        population = survivor_selection(population)       
    #hasil akhir
    best = population[0]
    x1, x2 = decode_chromosome(best)
    print(f"\nKromosom Terbaik: {best}, x1: {x1}, x2: {x2}, Fitness: {fitness_calc(best)}")

#inisialisasi populasi awal manual
initial_population = [
    "0111001011",
    "1000010001",
    "1000001110",
    "1001100000",
    "1010010011",
    "0110100001"
]

#run program
genetic_algorithm(5, initial_population)