# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from pylib.gtest import gtest_test_instance
from pylib.instrumentation import instrumentation_test_instance
from pylib.local.device import local_device_environment
from pylib.local.device import local_device_gtest_run
from pylib.local.device import local_device_instrumentation_test_run
from pylib.local.device import local_device_perf_test_run
from pylib.perf import perf_test_instance
from pylib.uirobot import uirobot_test_instance

try:
  from pylib.remote.device import remote_device_environment
  from pylib.remote.device import remote_device_gtest_run
  from pylib.remote.device import remote_device_instrumentation_test_run
  from pylib.remote.device import remote_device_uirobot_test_run
except ImportError:
  remote_device_environment = None
  remote_device_gtest_run = None
  remote_device_instrumentation_test_run = None
  remote_device_uirobot_test_run = None


def _CreatePerfTestRun(args, env, test_instance):
  if args.print_step:
    return local_device_perf_test_run.PrintStep(
        env, test_instance)
  elif args.output_json_list:
    return local_device_perf_test_run.OutputJsonList(
        env, test_instance)
  return local_device_perf_test_run.LocalDevicePerfTestRun(
      env, test_instance)


def CreateTestRun(args, env, test_instance, error_func):
  if isinstance(env, local_device_environment.LocalDeviceEnvironment):
    if isinstance(test_instance, gtest_test_instance.GtestTestInstance):
      return local_device_gtest_run.LocalDeviceGtestRun(env, test_instance)
    if isinstance(test_instance,
                  instrumentation_test_instance.InstrumentationTestInstance):
      return (local_device_instrumentation_test_run
              .LocalDeviceInstrumentationTestRun(env, test_instance))
    if isinstance(test_instance,
                  perf_test_instance.PerfTestInstance):
      return _CreatePerfTestRun(args, env, test_instance)

  if (remote_device_environment
      and isinstance(env, remote_device_environment.RemoteDeviceEnvironment)):
    # The remote_device modules should be all or nothing.
    assert (remote_device_gtest_run
            and remote_device_instrumentation_test_run
            and remote_device_uirobot_test_run)

    if isinstance(test_instance, gtest_test_instance.GtestTestInstance):
      return remote_device_gtest_run.RemoteDeviceGtestTestRun(
          env, test_instance)
    if isinstance(test_instance,
                  instrumentation_test_instance.InstrumentationTestInstance):
      return (remote_device_instrumentation_test_run
              .RemoteDeviceInstrumentationTestRun(env, test_instance))
    if isinstance(test_instance, uirobot_test_instance.UirobotTestInstance):
      return remote_device_uirobot_test_run.RemoteDeviceUirobotTestRun(
          env, test_instance)


  error_func('Unable to create test run for %s tests in %s environment'
             % (str(test_instance), str(env)))

