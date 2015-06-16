

import unittest
from cpuinfo import cpuinfo


class DataSource(object):
	bits = '64bit'
	cpu_count = 1
	is_windows = False
	raw_arch_string = 'amd64'

	@staticmethod
	def has_proc_cpuinfo():
		return False

	@staticmethod
	def has_dmesg():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		return 1, None

	@staticmethod
	def cpufreq_info():
		return 1, None

	@staticmethod
	def sestatus_allow_execheap():
		return False

	@staticmethod
	def sestatus_allow_execmem():
		return False

	@staticmethod
	def dmesg_a_grep_cpu():
		retcode = 0
		output = "CPU: Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz (2993.39-MHz K8-class CPU)"
		return retcode, output

	@staticmethod
	def dmesg_a_grep_origin():
		retcode = 0
		output = '  Origin = "GenuineIntel"  Id = 0x306c3  Family = 0x6  Model = 0x3c  Stepping = 3'
		return retcode, output

	@staticmethod
	def dmesg_a_grep_features():
		retcode = 0
		output = '  Features=0x78bfbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,CLFLUSH,MMX,FXSR,SSE,SSE2>'
		return retcode, output

	@staticmethod
	def sysctl_machdep_cpu_hw_cpufrequency():
		return 1, None

	@staticmethod
	def isainfo_vb():
		return 1, None

	@staticmethod
	def kstat_m_cpu_info():
		return 1, None




class TestPCBSD(unittest.TestCase):
	def test_all(self):
		cpuinfo.DataSource = DataSource

		info = cpuinfo.get_cpu_info_from_dmesg()

		self.assertEqual('GenuineIntel', info['vendor_id'])
		#self.assertEqual('', info['hardware'])
		self.assertEqual('Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz', info['brand'])
		self.assertEqual('3.1000 GHz', info['hz_advertised'])
		self.assertEqual('3.1000 GHz', info['hz_actual'])
		self.assertEqual((3100000000, 0), info['hz_advertised_raw'])
		self.assertEqual((3100000000, 0), info['hz_actual_raw'])
		self.assertEqual('X86_64', info['arch'])
		self.assertEqual(64, info['bits'])
		self.assertEqual(1, info['count'])

		self.assertEqual('x86_64', info['raw_arch_string'])

		self.assertEqual('6144 KB', info['l2_cache_size'])
		self.assertEqual(0, info['l2_cache_line_size'])
		self.assertEqual(0, info['l2_cache_associativity'])

		self.assertEqual(5, info['stepping'])
		self.assertEqual(30, info['model'])
		self.assertEqual(6, info['family'])
		self.assertEqual(0, info['processor_type'])
		self.assertEqual(0, info['extended_model'])
		self.assertEqual(0, info['extended_family'])
		self.assertEqual(
			['apic', 'clflush', 'cmov', 'constant_tsc', 'cx8', 'de', 'fpu', 
			'fxsr', 'ht', 'lahf_lm', 'lm', 'mca', 'mce', 'mmx', 'msr', 'mtrr', 
			'nopl', 'nx', 'pae', 'pat', 'pge', 'pni', 'pse', 'pse36', 'rdtscp', 
			'rep_good', 'sep', 'sse', 'sse2', 'ssse3', 'syscall', 'tsc', 'vme']
			,
			info['flags']
		)



