
from kivy.logger import Logger, LOG_LEVELS

# As well as the standard logging levels (debug, info, warning, error and critical), an additional trace level is available.
	# Logger.info('title: This is a info message.')
	# Logger.debug('title: This is a debug message.')
	#
	# try:
	#     raise Exception('bleh')
	# except Exception:
	#     Logger.exception('Something happened!')

class AppLogger:

	def log(msgloglevel, prefix, *messagelist):

		# Logger.debug("AppLogger.log")
		# Logger.debug(msgloglevel)

		lggrfn = {"debug": Logger.debug, "info": Logger.info, "warning": Logger.warning, "error": Logger.error, "critical": Logger.critical, "trace": Logger.trace,"exception": Logger.exception }

		# newmessagelist = [ i for each in messagelist str(i)]
		smessage = prefix + ": " +" ".join(str(msgpart) for msgpart in messagelist)

		# Logger.debug(smessage)

		lggrfn[msgloglevel.lower()](smessage)
