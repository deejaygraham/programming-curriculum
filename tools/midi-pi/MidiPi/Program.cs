using NAudio.Midi;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MidiPi
{
	class Program
	{
		static int Main(string[] args)
		{
			if (args.Length == 0)
			{
				Console.WriteLine("No midi file specified");
				return -1;
			}

			string midiFilePath = args[0];

			if (!File.Exists(midiFilePath))
            {
				Console.WriteLine("Cannot find midi file {0}", midiFilePath);
				return -1;
			}

			string outputFile = midiFilePath + ".spi";

			MidiFile midi = new MidiFile(midiFilePath);

			bool showMetaEvents = true;
			bool showUnknownEvents = false;
			bool showCalculations = false;

			int ticksPerQuarterNote = midi.DeltaTicksPerQuarterNote;
			double microsecondsPerQuarterNote = 500000f;

			using (var writer = new StreamWriter(outputFile, append: false))
			{
				writer.WriteLine("# Sonic Pi source code generated from {0}", Path.GetFileName(midiFilePath));

				if (showCalculations)
				{
					writer.WriteLine("# Tracks: {0}", midi.Tracks);

					for (int track = 0; track < midi.Tracks; ++track)
					{
						writer.WriteLine("# \tTrack {0} contains {1} events", track, midi.Events[track].Count());
					}
				}

				writer.WriteLine();

				// always process first track...
				for (int track = 0; track < midi.Tracks; ++track)
				{
					writer.WriteLine();
					writer.WriteLine("# Track {0} ", track);

					foreach (MidiEvent @event in midi.Events[track])
					{
						switch (@event.CommandCode)
						{
							case MidiCommandCode.NoteOn:
								{
									NoteOnEvent noteOn = @event as NoteOnEvent;

									if (noteOn != null)
									{
										// accumulate notes played at the same time?
										writer.WriteLine("play :{1} # {0}", noteOn.NoteNumber, noteOn.NoteName.Replace("#", "s"));

										if (noteOn.DeltaTime > 0)
										{
											writer.WriteLine("sleep {0}", DeltaTimeInSeconds(microsecondsPerQuarterNote, ticksPerQuarterNote, noteOn.DeltaTime));
										}
									}
								}
								break;

							case MidiCommandCode.MetaEvent:

								if (showMetaEvents)
								{
									MetaEvent meta = @event as MetaEvent;

									if (meta != null)
									{
										switch(meta.MetaEventType)
										{
											case MetaEventType.TimeSignature:
												{
													TimeSignatureEvent tse = meta as TimeSignatureEvent;

													writer.WriteLine("# {0}", tse.ToString());
												}
												break;

											case MetaEventType.SequenceTrackName:
												{
													TextEvent te = meta as TextEvent;

													writer.WriteLine("# Track Name: {0}", te.Text);
												}
												break;

											case MetaEventType.SetTempo:
												{
													TempoEvent te = meta as TempoEvent;

													microsecondsPerQuarterNote = te.MicrosecondsPerQuarterNote;
                                                    writer.WriteLine("use_bpm {0}", Math.Floor(te.Tempo));
                                                }
												break;
										}
									}
								}
								break;
							
							default:

								if (showUnknownEvents)
									writer.WriteLine("# unknown command {0}", @event.ToString());
								break;
						}
					}
				}
			}

			return 0;
		}

		private static double DeltaTimeInSeconds(double microsecondsPerQuarterNote, int ticksPerQuarterNote, int deltaTime)
		{
			double secondsPerQuarterNote = microsecondsPerQuarterNote / 1000000.0f;
			double secondsPerTick = secondsPerQuarterNote / ticksPerQuarterNote;

			return deltaTime * secondsPerTick;
		}
	}
}
