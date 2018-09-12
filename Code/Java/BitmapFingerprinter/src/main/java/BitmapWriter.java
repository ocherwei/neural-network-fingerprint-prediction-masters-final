import org.openscience.cdk.DefaultChemObjectBuilder;
import org.openscience.cdk.AtomContainer;
import org.openscience.cdk.exception.CDKException;
import org.openscience.cdk.exception.InvalidSmilesException;
import org.openscience.cdk.fingerprint.BitSetFingerprint;
import org.openscience.cdk.fingerprint.IBitFingerprint;
import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.layout.StructureDiagramGenerator;
import org.openscience.cdk.renderer.AtomContainerRenderer;
import org.openscience.cdk.renderer.font.AWTFontManager;
import org.openscience.cdk.renderer.generators.BasicAtomGenerator;
import org.openscience.cdk.renderer.generators.BasicBondGenerator;
import org.openscience.cdk.renderer.generators.BasicSceneGenerator;
import org.openscience.cdk.renderer.visitor.AWTDrawVisitor;
import org.openscience.cdk.silent.SilentChemObjectBuilder;
import org.openscience.cdk.smiles.SmilesParser;
import org.openscience.cdk.templates.MoleculeFactory;
import org.openscience.cdk.fingerprint.SubstructureFingerprinter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.BitSet;

public class BitmapWriter {

    private SmilesFile[] smilesList;

    public BitmapWriter(SmilesFile[] smilesList)
    {
        this.smilesList = smilesList;
    }

    public void writeBitmap()
    {
        SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
        SubstructureFingerprinter fp = new SubstructureFingerprinter();
        for(SmilesFile smiles: smilesList)
        {
            IAtomContainer mol = null;
            try
            {
                mol = sp.parseSmiles(smiles.getSmiles());

            }
            catch(InvalidSmilesException e)
            {
                //Do nothing
            }

            try{
                String filename = "E:/Development Project/Data/Fingerprint Bitmaps 2/";
                String fileEnd = smiles.getF().getName().replaceAll(".ms", ".txt");
                filename = filename + fileEnd;
                FileWriter writer = new FileWriter(filename);
                IBitFingerprint bfp = fp.getBitFingerprint(mol);
                // BitSet bs = bfp.asBitSet();  // May need to skip this step for accuracy. Seems to drop bits in minority of cases
//                if(bfp.size()<307)
//                {
//                    System.err.println(filename);
//                }
//                if(bs.length()<307)
//                {
//                    System.err.println(filename);
//                    System.err.println(bfp.size());
//                    System.err.println(bs.length());
//                }
                for(int i = 0; i<bfp.size(); i++)
                {
                    boolean currentBit = bfp.get(i);
                    if(currentBit == true)
                    {
                        writer.write("1");
                    }
                    else
                    {
                        writer.write("0");
                    }
                    writer.write("\n");
                }
                writer.close();


            }
            catch(CDKException e)
            {
                System.err.println("CDK Exception");
            }
            catch(IOException e)
            {
                e.printStackTrace();
                System.err.println("IOException");
            }




        }
    }
}
