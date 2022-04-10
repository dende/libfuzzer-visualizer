import fileinput

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from pyvis.network import Network
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def setup():
    fig, ax = plt.subplots()

    line, = ax.plot([0], [0], 'r-')  # Returns a tuple of line objects, thus the comma
    plt.ion()
    plt.show()

    ax2 = ax.twinx()
    ax.set_xlabel('iterations')
    ax.set_ylabel('cov:', color='r')
    ax2.set_ylabel('ft:', color='b')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    line2, = ax2.plot([0], [0], 'b-')  # Returns a tuple of line objects, thus the comma

    net = Network(directed=True, height=720, width=1280)
    net.barnes_hut()
    net.add_node("0.0", "LLVMFuzzerTestOneInput()", size=10)
    net.add_node("0.1", "YAML::Load()", size=40)
    net.add_edge("0.0", "0.1")
    return ax, ax2, line, line2, net


def main():
    iterations = [0]
    coverages = [0]
    features = [0]
    ax, ax2, line, line2, net = setup()

    num_entryfuns = 0
    funcs = []

    try:

        for inputline in fileinput.input():
            print(inputline, end="")
    #    for inputline in testdata.split("\n"):
            inputline = inputline.strip()
            plt.pause(0.01)

            if inputline.startswith("INFO:"):
                continue
            if inputline.startswith("#"):
                parts = inputline.split()
                iteration = int(parts[0][1:])
                type = parts[1]
                coverage = int(parts[3])
                feature = int(parts[5])
                corpus = parts[7]
                lim = parts[9]
                execs = parts[11]
                iterations.append(iteration)
                coverages.append(coverage)
                features.append(feature)


            if inputline.startswith("NEW_FUNC"):

                parts = inputline.split()
                nums = [int(s) for s in parts[0][9:-2].split("/")]
                fun = parts[3]
                loc = parts[4]

                funcs.append((fun, loc))

                if nums[0] == 1:
                    num_entryfuns += 1
                elif nums[0] == nums[1]:
                    pass

                net.add_node(n_id=f"{num_entryfuns}.{nums[0]}", label=fun)

                if nums[0] > 1:
                    net.add_edge(f"{num_entryfuns}.{nums[0] - 1}", f"{num_entryfuns}.{nums[0]}")
                elif nums[0] == 1:
                    net.add_edge(f"0.1", f"{num_entryfuns}.{nums[0]}")

            line.set_ydata(coverages)
            line.set_xdata(iterations)
            line2.set_ydata(features)
            line2.set_xdata(iterations)
            ax.relim()
            ax2.relim()
            # update ax.viewLim using the new dataLim
            ax.autoscale_view()
            ax2.autoscale_view()

            plt.draw()

    except KeyboardInterrupt:
        pass
    finally:
        net.show(f"{dir_path}/coverage.html")
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
