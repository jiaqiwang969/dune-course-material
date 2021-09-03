#include "config.h"

#include <regex>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <vector>
#include <chrono> //计时

#ifdef __linux__
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#elif __APPLE__
#include <sys/types.h>
#include <sys/sysctl.h>
#endif

#include <dune/codegen/common/tsc.hh>

namespace Dune
{
  namespace PDELab
  {

    namespace impl
    {

#if __linux__

      TSC::Counter get_tsc_frequency_from_dmesg()
      {
        int pipe_fds[2];
        if (pipe(pipe_fds) < 0)
          DUNE_THROW(TSCError, "Failed to create pipe for communicating with dmesg");

        pid_t pid = fork();

        if (pid < 0)
          DUNE_THROW(TSCError, "Failed to fork process for running dmesg");

        double result = -1.0;

        if (pid == 0)
        {
          if (close(0) < 0)
            _exit(1);

          if (close(2) < 0)
            _exit(2);

          if (dup2(pipe_fds[1], 1) < 0)
            _exit(3);

          if (close(pipe_fds[0]) < 0)
            _exit(4);

          if (close(pipe_fds[1]) < 0)
            _exit(5);

          const char *args[] = {
              "/bin/dmesg",
              "-t",
              nullptr};
          execvp(args[0], const_cast<char *const *>(args));

          _exit(6);
        }

        if (pid > 0)
        {

          if (close(pipe_fds[1]) < 0)
            DUNE_THROW(TSCError, "Failed to close write end of pipe");

          std::regex regex("tsc:.*TSC.*?(\\d+\\.\\d+)\\s+MHz\n");

          FILE *input = fdopen(pipe_fds[0], "r");

          if (not input)
            DUNE_THROW(TSCError, "Failed to create file object for reading dmesg output");

          char buf[1024];
          std::cmatch match;

          while (fgets(buf, 1024, input))
          {
            if (std::regex_match(buf, match, regex))
            {
              result = atof(match[1].first);
              break;
            }
          }

          if (fclose(input) != 0)
            DUNE_THROW(TSCError, "Failed to close file object for reading dmesg output");

          int status;
          if (waitpid(pid, &status, 0) < 0)
            DUNE_THROW(TSCError, "Failed to clean up dmesg child process");

          // if (WEXITSTATUS(status) != 0)
          //   DUNE_THROW(TSCError,"Child process failed with return status " << WEXITSTATUS(status));

          if (result < 0)
            DUNE_THROW(TSCNotInKernelLog, "Could not find TSC frequency information in kernel log");
        }

        // The kernel logs the frequency in MHz
        return static_cast<TSC::Counter>(result * 1e6);
      }

      TSC::Counter get_tsc_frequency_from_cpuinfo()
      {
        double result = -1.0;
        try
        {
          std::ifstream cpuinfo("/proc/cpuinfo");
          auto re = std::regex("bogomips\\s:\\s(\\d+\\.\\d+)$");

          auto match = std::smatch();
          using std::getline;
          for (std::string line; getline(cpuinfo, line);)
          {
            if (std::regex_match(line, match, re))
            {
              result = 5e5 * std::stod(match[1].str());
              break;
            }
          }
        }
        catch (std::exception &e)
        {
          DUNE_THROW(TSCError, "error getting TSC frequency from /proc/cpuinfo: " << e.what());
        }

        if (result < 0)
          DUNE_THROW(TSCError, "could not find bogomips value in /proc/cpuinfo");

        return result;
      }

      TSC::Counter get_tsc_frequency()
      {
        try
        {
          return get_tsc_frequency_from_dmesg();
        }
        catch (TSCNotInKernelLog &)
        {
          return get_tsc_frequency_from_cpuinfo();
        }
      }

#elif __APPLE__

      TSC::Counter get_tsc_frequency()
      {
        std::int64_t frequency = 0;
        std::size_t size = sizeof(frequency);
        if (sysctlbyname("machdep.tsc.frequency", &frequency, &size, nullptr, 0) < 0)
          DUNE_THROW(TSCError, "Failed to read TSC frequency from sysctl machdep.tsc.frequency");
        return frequency;
      }

#endif

      TSC::Counter calibrate_tsc_overhead_min(std::size_t iterations)
      {
        typedef std::ratio<1, 3200000000> period; // My mac @ 3.2 GHz

        TSC::Counter overhead = std::numeric_limits<TSC::Counter>::max();

        for (std::size_t i = 0; i < iterations; ++i)
        {
          // start = TSC::start();
          auto start = std::chrono::high_resolution_clock::now();
          asm volatile("");

          // end = TSC::stop();
          auto end = std::chrono::high_resolution_clock::now();

          std::chrono::duration<double, period> elapsed_seconds = end - start;

          overhead = std::min(unsigned(overhead), unsigned(elapsed_seconds.count()));
        }

        return overhead;
      }

      TSC::Counter calibrate_tsc_overhead_median(std::size_t iterations)
      {
        //TSC::Counter start, end;
        typedef std::ratio<1, 3200000000> period; // My mac @ 3.2 GHz

        std::vector<TSC::Counter> measurements(iterations);

        for (auto &m : measurements)
        {
          //start = TSC::start();
          //auto start = std::chrono::steady_clock::now();
          auto start = std::chrono::high_resolution_clock::now();
          asm volatile("");
          //end = TSC::stop();
          // auto end = std::chrono::steady_clock::now();
          auto end = std::chrono::high_resolution_clock::now();

          //m = end - start;
          std::chrono::duration<double, period> elapsed_seconds = end - start;
          m = unsigned(elapsed_seconds.count());
        }

        std::sort(measurements.begin(), measurements.end());
        return measurements[measurements.size() / 2];
      }

    } // namespace impl

    TSC::TSC(const Dune::ParameterTree *params)
    {
      if (params)
      {
        if (params->hasKey("frequency"))
          _frequency = params->get<TSC::Counter>("frequency");
        else
          _frequency = impl::get_tsc_frequency();
        _scale_factor = 1.0 / _frequency;

        if (params->get<bool>("correct_overhead", true))
        {
          std::string calibration_method = params->get<std::string>("calibration_method", "min");
          if (calibration_method == "min")
            _overhead = impl::calibrate_tsc_overhead_min(params->get<std::size_t>("calibration_iterations", TSC::calibrationIterations()));
          else if (calibration_method == "median")
            _overhead = impl::calibrate_tsc_overhead_median(params->get<std::size_t>("calibration_iterations", TSC::calibrationIterations()));
          else
            DUNE_THROW(TSCError, "Unknown TSC calibration method " << calibration_method);
        }
        else
          _overhead = 0;
      }
      else
      {
        _frequency = impl::get_tsc_frequency();
        _overhead = impl::calibrate_tsc_overhead_min(TSC::calibrationIterations());
      }
      _scale_factor = 1.0 / _frequency;
    }

    // initialize with something stupid
    TSC::Counter TSC::_overhead = std::numeric_limits<TSC::Counter>::max();

  } // namespace PDELab
} // namespace Dune
