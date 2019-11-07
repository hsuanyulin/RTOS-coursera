"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler
import math


@scheduler("simso.schedulers.P_RM")
class P_RM(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.RM_mono"))

    def packer(self):
        # First Fit
        cpus = [[cpu, 0, 1.0] for cpu in self.processors]
        for task in self.task_list:
            j = 0
            # Find a processor with free space.
            while cpus[j][1] + float(task.wcet) / task.period > cpus[j][2]*(math.pow(2, 1/cpus[j][2])-1):
                j += 1

                if j >= len(self.processors):
                    print("oops Scheduling failed.")
                    return False


            # Affect it to the task.
            self.affect_task_to_processor(task, cpus[j][0])

            # Update utilization.
            cpus[j][1] += float(task.wcet) / task.period
            cpus[j][2] += 1.0
        return True
