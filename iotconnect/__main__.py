import time
import json
import logging
import logging.config
from importlib import import_module
from .__version__ import __version__
from .publisher import PublisherError
from .monitor import MonitorError


def load_class(module_class):
    qname = module_class.split('.')
    length = len(qname)
    clazz = qname[length-1]
    module = ""
    for i in range(length-1):
        module += qname[i] + "."

    module = module.rstrip('.')
    return getattr(import_module(module), clazz)


def main():
    """Starts all the publishers and monitors and control the status periodically."""
    logger = logging.getLogger('iotconnect')
    logging.config.fileConfig('iotconnect/logging.conf')
    try:
        logger.info('======================= Starting IOTConnect (v%s) =======================' % __version__)
        Monitors = []
        Publishers = []
        try:
            with open('iotconnect/iotconnect.config.json') as config_file:
                config = json.loads(config_file.read())
        except (FileNotFoundError):
            raise Exception('Config file not found')
        except json.decoder.JSONDecodeError as err:
            raise Exception('Error parsing config file: %s', err)

        # Load the publishers
        logger.info('=== Loading publishers ===')
        for pub_config in config['publishers']:
            try:
                logger.info('Loading publisher for class %s...',
                            pub_config['class'])
                Publisher = load_class(pub_config['class'])
                pub_instance = Publisher(pub_config)
                pub_instance.initialize()
                Publishers.append(pub_instance)
                logger.info('%s loaded', pub_instance.__class__.__name__)
            except (Exception) as err:
                logger.error('Error loading publisher for class %s. %s',
                             pub_config['class'], err)

        if len(Publishers) == 0:
            raise PublisherError("No publishers loaded")

        # Load the monitors
        logger.info('=== Loading monitors ===')
        for monitor_config in config['monitors']:
            try:
                logger.info('Loading monitor for class %s',
                            monitor_config['class'])
                Monitor = load_class(monitor_config['class'])
                monitor_instance = Monitor(monitor_config, Publishers)
                Monitors.append(monitor_instance)
                logger.info('%s loaded', monitor_instance.__class__.__name__)
            except (Exception) as err:
                logger.error('Error loading monitor for class %s. %s',
                             monitor_config['class'], err, exc_info=False)

        if len(Monitors) == 0:
            raise MonitorError("No monitors loaded")

        main_running = True
        try:
            while main_running:
                state_info = {'timestamp': int(round(time.time())),
                              'state': 'running'}
                monitors_state_info = []
                # Check monitors statate and start them if stopped
                for mon in Monitors:
                    status = mon.check_thread()
                    if not status:
                        logger.warning('%s not started', mon.__class__.__name__)
                        try:
                            mon.start()
                        except Exception as ex:
                            logger.error('Error starting %s. %s',
                                         mon.__class__.__name__, ex)
                    monitors_state_info.append({mon.__class__.__name__: 'started' if mon.check_thread() else 'stopped'})
                    state_info.update({'monitors': monitors_state_info})
                # Publish monitors states to all configured publishers and initialize publishers not initialized before.
                for pub in Publishers:
                    try:
                        if not pub.is_initialized():
                            logger.warning('%s not initialized', pub.__class__.__name__)
                            pub.initialize()

                        pub.publish('state', state_info)
                    except Exception as ex:
                        logger.error('Error publishing %s. %s',
                                     pub.__class__.__name__, ex)

                # Wait some time before cheking again the monitors
                time.sleep(15)
        except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
            main_running = False
        except Exception as ex:
            main_running = False
            logger.error('Unexpected error: {}'.format(ex), exc_info=False)
        finally:
            logger.info('=== Stopping monitors ===')
            for pl in Monitors[::-1]:  # reverse monitors
                pl.stop()
            logger.info('=== Closing publishers ===')
            for pb in Publishers:
                pb.close()
    except (MonitorError, PublisherError) as err:
        logger.error('IOTConnect execution aborted. {}'.format(err))
    except Exception as ex:
        logger.error('Unexpected error: {}'.format(ex), exc_info=True)
    finally:
        logger.info('======================= IOTConnect stopped =======================')


if __name__ == '__main__':
    main()
