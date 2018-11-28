# Evolutionary_Bridge_Designer
A set of programs that use evolution to design high-load bearing bridges. The bridges are designed to survive under the load pattern of the Baldwin press at the University of Toronto.

## The Basic Idea:
Here are the core elements of the original assignment:
* We have a finite amount of matboard
* We learned several formulae for calculating the loads that various bridge shapes are able to bear
* We must now design a bridge that does not exceed the given amount of matboard, and that can withstand the maximum load.

To me, this immediately seemed like an optimization problem. You are trying to find the parameters for your bridge that will yield the maximum (optimal) load bearing ability, while not using too much board.

But how should I go about optimizing this? There are a bunch of cool ways to optimize these sorts of situations, but the simplest one that I've used so far is evolution. Like in biological evolution, the fittest organisms reproduce and hence the fitness of future generations is improved. In the case of this program, the "organism" is a set of parameters that describe a bridge, the fitness function is the function that tells you how much weight a bridge can bear, and reproduction is where you make a slightly "mutated" copy of a bridge (all the parameters are changed by a random degree).

So here's what the process looks like: you start with one bridge design (lets call it `champ`), and you make a mutated copy of it (call it `mutant`). If the amount of weight that `mutant` can bear is greater than the weight that `champ` can, then copy parameters of `mutant` to `champ` (else we let `champ` continue as is without changing parameters). We then repeat the process, making more copies of `champ` and replacing `champ` if the `mutant` bridge is better. This process goes on for as many generations as the user specifies.

Evolution is a really fun way to get introduced to optimization! Compared to more advanced techniques, it's pretty computationally inefficient, but it works reasonably well for this exercise. If you're interested in a deeper look at evolution in computer programming, check out the wikipedia page! Another good evolution method to look into is you're interested is called gradient descent (used a lot in machine learning). I hope to make a version of this program that uses gradient descent some time in the future and compare the results with the evolutionary approach

## Dependencies:
These programs use the `math`, `random`, `tqdm`, and `copy` python modules. `tqdm` is simply used to make nice progress bars so you can watch evolution happen in real time :)

## Descriptions of Scripts:
* `bridgelib.py` contains a preliminary set of functions to calculate simple central point-load bearing abilities of a uniform cross section pi-beam.
* `bridgelib2.py` contains a more advanced set of functions to calculate the load-bearing abilities of a bridge with two cross sections that has two point loads located at 550mm and 1250mm from the left side. Section A of the beam is a pi-beam and section B is a boxed beam. The beam cross section changes at 798mm from the left side.
* `bridge_evolver.py` implements evolution to optimize the bridge parameters.
* `bridge_calculator.py` is a testing space of sorts where one can manually enter bridge parameters and determine the load bearing ability.

## Descriptions of Major Functions in `bridgelib2.py`:
* `Bridge.get_I_A()` and `Bridge.get_I_B()` calculate the I value (moment of inertia) for the A and B section of a given bridge design respectively.
* `Bridge.get_centroid_A()` and `Bridge.get_centroid_A()` calculate the centroid for the A and B section of a given bridge design respectively.
* `Bridge.get_midspan_deflection()` is a depreciated method for find the midspan deflection of a bridge under a single, central point load. It does not work for the baldwin loading style.
* `Bridge.get_max_P_flexural_A()` and `bridge.get_max_P_flexural_B()` return a list [P1, P2] where P1 is the load that will cause a tension failure and P2 is the load that will cause a compressive failure in the bridge.
* `Bridge.get_max_P_shear_A()` and `Bridge.get_max_P_shear_B()` return the load that will cause a shear failure in the A and B sections respectively.
* `Bridge.get_buckling_failure_A()` and `Bridge.get_buckling_failure_B()` return a list [P1, P2, P3, P4] where P1 is the load causing compressive flange buckling failure, P2 is the load causing buckling at the top of the web, P3 is the load causing shear buckling at the top of the web, and P4 is the load causing compressive buckling at the edge of the flange.

* `Bridge.get_amount_paper()` gives the amount of matboard (in mm^2) that the bridge will require (does not include margins for tabs, error, etc.)
* `Bridge.is_valid()` determines the validity of a given design. It will return `False` if too much matboard is used, or if the flange width is less than the web distance, or if the flange width is less than 100 mm (as per assignment requirements).

* `Bridge.get_max_load_A()` gives the minimum load that will cause **some** failure in section A of the bridge.
* `Bridge.get_max_load_B()` gives the minimum load that will cause **some** failure in section B of the bridge.
* `Bridge.get_max_load()` gives the minimum load (P-value) that will cause **some** failure in the bridge as a whole.

* `Bridge.report()` gives a relatively nice report about the bridge, including all its relevant dimensions, failure loads, total load bearing ability, etc.

* `mutate(b)` returns a mutated version of Bridge b (as described above)
* `evolve(b, num_generations)` implements the evolutionary process described above starting with the bridge `b` and taking `num_generations` generations. It returns an optimized bridge.

## Cool Things to Consider:
#### Multiple Optimae:
If you imagined making the many dimensional plot of all bridge parameters against the `Bridge.get_max_load()` function for the bridge defined by the bridge paramters at a given point, what would that function look like? This program is trying to use evolution to find peaks in that function. But how many peaks are there? Are there multiple equally good bridge designs? Or is there one that is dramatically better? 

#### Plotting `Bridge.get_max_load()` Over the Course of Evolution
When you evolve bridges, is it relatively smooth sailing overall? Or are there massive leaps and innovations in bridge design, or are there massive stagnations in the middle of the program?

#### How Should one Define the Fitness Function in the Real World?
I was talking with Professor Collins about this project, and he said there was significant interest in this type of design process when the computing power was first becoming available for this type of computation. However, he said that one of the big issues was about how to define the Fitness (or, as some people like to refer to it, the **cost** function) should be defined.

Should we be maximizing for total load bearing ability? Or cost of the materials? Or how easy it is to build? How quickly it can be built? How should we balance all of these goals? How can that be encoded programmatically? 
